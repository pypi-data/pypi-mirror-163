# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the SG Otio project

import logging
from collections import defaultdict

from .sg_settings import SGShotFieldsConfig
from .clip_group import ClipGroup
from .constants import _DIFF_TYPES
from .cut_clip import SGCutClip
from .cut_diff import SGCutDiff
from .utils import compute_clip_shot_name, get_entity_type_display_name

logger = logging.getLogger(__name__)


# Some counts are per Shot, some others per edits
# As a rule of thumb, everything which directly affects the Shot is per
# Shot:
# - Creation of new Shots (NEW)
# - Omission of existing Shots (OMITTED)
# - Re-enabling existing Shots (REINSTATED)
# - Need for a rescan (RESCAN)
# On the other hand, in and out point changes, some repeated Shots being
# added or removed are counted per item and are considered CUT_CHANGES
_PER_SHOT_TYPE_COUNTS = [
    _DIFF_TYPES.NEW,
    _DIFF_TYPES.OMITTED,
    _DIFF_TYPES.REINSTATED,
    _DIFF_TYPES.RESCAN
]


# Template used by summary report
_BODY_REPORT_FORMAT = """
%s
Links: %s

The changes in %s are as follows:

%d New Shots
%s

%d Omitted Shots
%s

%d Reinstated Shot
%s

%d Cut Changes
%s

%d Rescan Needed
%s

"""


class SGCutDiffGroup(ClipGroup):
    """
    A class representing groups of Cut differences.
    """
    def __init__(self, name, clips=None, sg_shot=None):
        """
        Override base implementation to add members we need.
        """
        super(SGCutDiffGroup, self).__init__(name, clips, sg_shot)
        self._old_earliest_clip = None
        self._old_last_clip = None

    @property
    def clips(self):
        """
        Returns the clips that are part of the group and are not omitted entries.

        :yields: :class:`SGCutClip` instances.
        """
        # Don't return the original list, because it might be modified.
        for clip in self._clips:
            if clip.current_clip:
                yield clip

    def add_clip(self, clip):
        """
        Adds a Cut difference to the group.

        Override base implementation to deal with ommitted entries.

        :param clip: A :class:`SGCutDiff` instance.
        """
        if not clip.current_clip:
            # Just append the clip without affecting the group values.
            self._append_clip(clip)
            if self._old_earliest_clip is None or clip.source_in < self._old_earliest_clip.source_in:
                self._old_earliest_clip = clip
            if self._old_last_clip is None or clip.source_out > self._old_last_clip.source_out:
                self._old_last_clip = clip
            logger.debug(
                "Added omitted clip %s %s %s" % (clip.name, clip.cut_in, clip.cut_out)
            )
            return

        # Just call the base implementation
        super(SGCutDiffGroup, self).add_clip(clip)

    @property
    def earliest_clip(self):
        """
        Return the earliest Clip in this group.

        :returns: A :class:`sg_otio.SGCutClip`.
        """
        # We might have a mix of omitted edits (no new value) and non omitted edits
        # (with new values) in our list. If we have at least one entry which is
        # not omitted (has new value) we consider entries with new values, so we
        # will consider omitted edits only if all edits are omitted
        if self._earliest_clip:
            return self._earliest_clip
        return self._old_earliest_clip

    @property
    def last_clip(self):
        """
        Return the last Clip in this group.

        :returns: A :class:`sg_otio.SGCutClip`.
        """
        # We might have a mix of omitted edits (no new value) and non omitted edits
        # (with new values) in our list. If we have at least one entry which is
        # not omitted (has new value) we consider entries with new values, so we
        # will consider omitted edits only if all edits are omitted
        if self._last_clip:
            return self._last_clip
        return self._old_last_clip

    @property
    def sg_shot_is_omitted(self):
        """
        Return ``True`` if the SG Shot for this group does not appear in the
        Cut anymore.

        :returns: ``False``, this can only be checked when comparing to another
                  Cut where the Shot was present.
        """
        for cut_diff in self:
            if cut_diff.diff_type == _DIFF_TYPES.OMITTED:
                return True
            elif cut_diff.diff_type == _DIFF_TYPES.OMITTED_IN_CUT:
                return False
        # If we reached that point it's because all entries are omitted in cut.
        return True

    def get_shot_values(self):
        """
        Loop over our Cut diff list and return values which should be set on the
        Shot.

        The Shot difference type can be different from individual Cut difference
        types, for example a new edit can be added, but the Shot itself is not
        new.

        Return a tuple with :
        - A SG Shot dictionary or None
        - The smallest cut order
        - The earliest head in
        - The earliest cut in
        - The last cut out
        - The last tail out
        - The Shot difference type

        :returns: A tuple
        """
        min_cut_order = None
        min_head_in = None
        min_cut_in = None
        max_cut_out = None
        max_tail_out = None
        sg_shot = None
        shot_diff_type = None
        # Do a first pass with all entries to get min and max
        for cut_diff in self:
            if sg_shot is None and cut_diff.sg_shot:
                sg_shot = cut_diff.sg_shot
            cut_order = cut_diff.index
            if cut_order is not None and (min_cut_order is None or cut_order < min_cut_order):
                min_cut_order = cut_order
            if cut_diff.head_in is not None and (
                    min_head_in is None or cut_diff.head_in < min_head_in):
                min_head_in = cut_diff.head_in
            if cut_diff.cut_in is not None and (
                    min_cut_in is None or cut_diff.cut_in < min_cut_in):
                min_cut_in = cut_diff.cut_in
            if cut_diff.cut_out is not None and (
                    max_cut_out is None or cut_diff.cut_out > max_cut_out):
                max_cut_out = cut_diff.cut_out
            if cut_diff.tail_out is not None and (
                    max_tail_out is None or cut_diff.tail_out > max_tail_out):
                max_tail_out = cut_diff.tail_out
        # We do a second pass for the Shot difference type, as we might stop
        # iteration at some point. Given that the number of duplicated shots is
        # usually low, there shouldn't be a big performance hit in iterating twice
        for cut_diff in self:
            # Special cases for diff type:
            # - A Shot is NO_LINK if any of its items is NO_LINK (should be all of them)
            # - A Shot is OMITTED if all its items are OMITTED
            # - A Shot is NEW if any of its items is NEW (should be all of them)
            # - A Shot is REINSTATED if at least one of its items is REINSTATED (should
            #       be all of them)
            # - A Shot needs RESCAN if any of its items need RESCAN
            cut_diff_type = cut_diff.diff_type
            if cut_diff_type in [
                _DIFF_TYPES.NO_LINK,
                _DIFF_TYPES.NEW,
                _DIFF_TYPES.REINSTATED,
                _DIFF_TYPES.OMITTED,
                _DIFF_TYPES.RESCAN
            ]:
                shot_diff_type = cut_diff_type
                # Can't be changed by another entry, no need to loop further
                break

            if cut_diff_type == _DIFF_TYPES.OMITTED_IN_CUT:
                # Could be a repeated Shot entry removed from the Cut
                # or really the whole Shot being removed
                if shot_diff_type is None:
                    # Set initial value
                    shot_diff_type = _DIFF_TYPES.OMITTED
                elif shot_diff_type == _DIFF_TYPES.NO_CHANGE:
                    shot_diff_type = _DIFF_TYPES.CUT_CHANGE
                else:
                    # Shot is already with the right state, no need to do anything
                    pass

            elif cut_diff_type == _DIFF_TYPES.NEW_IN_CUT:
                shot_diff_type = _DIFF_TYPES.CUT_CHANGE
            else:    # _DIFF_TYPES.NO_CHANGE, _DIFF_TYPES.CUT_CHANGE
                if shot_diff_type is None:
                    # initial value
                    shot_diff_type = cut_diff_type
                elif shot_diff_type != cut_diff_type:
                    # If different values fall back to CUT_CHANGE
                    # If values are identical, do nothing
                    shot_diff_type = _DIFF_TYPES.CUT_CHANGE
        # Having _OMITTED_IN_CUT here means that all entries were _OMITTED_IN_CUT
        # so the whole Shot is _OMITTED
        if shot_diff_type == _DIFF_TYPES.OMITTED_IN_CUT:
            shot_diff_type = _DIFF_TYPES.OMITTED
        return (
            sg_shot,
            min_cut_order,
            min_head_in,
            min_cut_in,
            max_cut_out,
            max_tail_out,
            shot_diff_type,
        )


class SGTrackDiff(object):
    """
    A class to compare a track to one read from SG.
    """
    def __init__(self, sg, sg_project, new_track, old_track=None):
        """
        Instantiate a new SGTrackDiff for the given SG Project.

        If an old track is provided it must have been read from SG with `sg`
        metadata populated for each of its Clips.

        :param sg: A connected SG handle.
        :param sg_project: A SG Project as a dictionary.
        :param new_track: A :class:`opentimelineio.schema.Track` instance.
        :param old_track: An optional :class:`opentimelineio.schema.Track` instance
                          read from SG.
        :raises ValueError: For invalid old tracks.
        """
        self._sg = sg
        self._sg_project = sg_project
        self._sg_entity = None
        self._sg_shot_link_field_name = None
        self._counts = defaultdict(int)
        self._total_count = 0

        self._diffs_by_shots = {}
        # Retrieve the Shot fields we need to query from SG.
        sg_shot_fields = SGShotFieldsConfig(
            self._sg, None
        ).all

        # Retrieve SG Entities from the old_track
        sg_shot_ids = []
        prev_clip_list = []
        if old_track:
            sg_cut = old_track.metadata.get("sg")
            if not sg_cut or sg_cut["type"] != "Cut":
                raise ValueError(
                    "Invalid track %s not linked to a SG Cut" % old_track.name
                )
            self._sg_entity = sg_cut.get("entity") or self._sg_project
            logger.debug("Previous SG Cut was linked to %s" % self._sg_entity)
            self._sg_shot_link_field_name = self._get_shot_link_field(self._sg_entity["type"])
            for i, clip in enumerate(old_track.each_clip()):
                # Check if we have some SG meta data
                sg_cut_item = clip.metadata.get("sg")
                if not sg_cut_item or sg_cut_item.get("type") != "CutItem":
                    raise ValueError(
                        "Invalid clip %s not linked to a SG CutItem" % clip.name
                    )
                sg_shot = sg_cut_item.get("shot")
                if sg_shot:
                    shot_id = sg_shot.get("id")
                    if shot_id:
                        sg_shot_ids.append(shot_id)
                prev_clip_list.append(
                    SGCutClip(clip, index=i + 1, sg_shot=sg_shot)
                )
            logger.debug(
                "Previous Cut list is %s" % ",".join(
                    ["%s (%s)" % (x.name, x.sg_shot) for x in prev_clip_list]
                )
            )
        # Add the linked Entity field to the fields to retrieve for Shots if
        # we have one from the previous Cut.
        if self._sg_shot_link_field_name:
            sg_shot_fields.append(self._sg_shot_link_field_name)

        sg_shots_dict = {}
        # Retrieve details for Shots linked to the Clips
        if sg_shot_ids:
            sg_shots = self._sg.find(
                "Shot",
                [["id", "in", list(sg_shot_ids)]],
                sg_shot_fields
            )
            # Build a dictionary where Shot names are the keys, use the Shot id
            # if the name is not set
            sg_shots_dict = dict(((x["code"] or str(x["id"])).lower(), x) for x in sg_shots)

        # Retrieve additional Shots from the new track if needed
        self._diffs_by_shots = {}
        more_shot_names = set()
        for i, clip in enumerate(new_track.each_clip()):
            shot_name = compute_clip_shot_name(clip)
            if shot_name:
                # Matching Shots must be case insensitive
                shot_name = shot_name.lower()
                more_shot_names.add(shot_name)
            # Ensure a SGCutDiffGroup and add SGCutDiff to it.
            if shot_name not in self._diffs_by_shots:
                self._diffs_by_shots[shot_name] = SGCutDiffGroup(shot_name)
            self._diffs_by_shots[shot_name].add_clip(
                SGCutDiff(clip=clip, index=i + 1, sg_shot=None)
            )
        if more_shot_names:
            filters = [
                ["project", "is", self._sg_project],
                ["code", "in", list(more_shot_names)]
            ]
            # If we have a linked SG Entity from a previous Cut, restrict
            # to Shots linked to this SG Entity.
            if self._sg_shot_link_field_name:
                filters.append(
                    [self._sg_shot_link_field_name, "is", self._sg_entity]
                )

            sg_more_shots = self._sg.find(
                "Shot",
                filters,
                sg_shot_fields,
            )

            for sg_shot in sg_more_shots:
                shot_name = sg_shot["code"].lower()
                self._diffs_by_shots[shot_name].sg_shot = sg_shot

        # Duplicate the list of shots, allowing us to know easily which ones are
        # not part of the new track by removing entries when we use them.
        # We only need a shallow copy here
        leftover_shots = [x for x in sg_shots_dict.values()]
        seen_names = []
        duplicate_names = {}
        logger.debug("Matching clips...")
        for shot_name, clip_group in self._diffs_by_shots.items():
            # Since we loop over all clips, take the opportunity to set their
            # repeated flag
            repeated = len(clip_group) > 1
            for clip in clip_group.clips:
                # Ensure unique names
                if clip.name not in seen_names:
                    seen_names.append(clip.name)
                else:
                    if clip.name not in duplicate_names:
                        duplicate_names[clip.name] = 0
                    duplicate_names[clip.name] += 1
                    clip.cut_item_name = "%s_%03d" % (clip.name, duplicate_names[clip.name])
                # If we don't have a Shot name we can't match anything
                if not shot_name:
                    logger.debug("No Shot name for %s, not matching..." % clip.cut_item_name)
                    continue
                clip.repeated = repeated
                logger.debug("Matching %s for %s (%s)" % (
                    shot_name, clip.cut_item_name, clip_group.sg_shot,
                ))
                # If we found a SG Shot, we can match with its id.
                if clip_group.sg_shot:
                    old_clip = self.old_clip_for_shot(
                        clip,
                        prev_clip_list,
                        clip_group.sg_shot,
                        clip.sg_version,
                    )
                    clip.old_clip = old_clip
                    # We still need to remove the Shot from leftovers
                    # Remove this entry from the leftovers
                    if clip_group.sg_shot in leftover_shots:
                        leftover_shots.remove(clip_group.sg_shot)
                else:
                    # Do we have a matching Shot in SG ?
                    matching_shot = sg_shots_dict.get(shot_name)
                    if matching_shot:
                        # yes we do
                        logger.debug("Found matching existing Shot %s" % shot_name)
                        # Remove this entry from the leftovers
                        if matching_shot in leftover_shots:
                            leftover_shots.remove(matching_shot)
                        else:
                            logger.warning("%s is not in existing Shots" % shot_name)
                        clip_group.sg_shot = matching_shot
                        old_clip = self.old_clip_for_shot(
                            clip,
                            prev_clip_list,
                            matching_shot,
                            clip.sg_version,
                        )
                        clip.old_clip = old_clip
        # Process clips left over, they are all the clips which were
        # not matched to a clip from the new track.
        for clip in prev_clip_list:
            logger.info("Processing un-matched old clip %s" % clip.cut_item_name)
            clip_sg_shot = clip.sg_shot
            # If no Shot, we don't really care about it
            if not clip_sg_shot:
                logger.debug("Ignoring old clip %s with no SG Shot" % (clip.cut_item_name))
                continue
            shot_name = "No Link"
            matching_shot = None
            for sg_shot in sg_shots_dict.values():
                if sg_shot["id"] == clip_sg_shot["id"]:
                    # We found a matching Shot
                    shot_name = sg_shot["code"]
                    logger.debug(
                        "Found matching existing Shot %s" % shot_name
                    )
                    matching_shot = sg_shot
                    # Remove this entry from the list
                    if sg_shot in leftover_shots:
                        logger.debug("Removing %s from leftovers..." % sg_shot)
                        leftover_shots.remove(sg_shot)
                    break

            repeated = False
            if shot_name not in self._diffs_by_shots:
                self._diffs_by_shots[shot_name] = SGCutDiffGroup(
                    shot_name,
                    sg_shot=matching_shot
                )
            else:
                repeated = True
                for clip2 in self._diffs_by_shots[shot_name].clips:
                    clip2.repeated = True

            self._diffs_by_shots[shot_name].add_clip(
                SGCutDiff(
                    clip=clip.clip,
                    index=clip.index,
                    sg_shot=clip.sg_shot,
                    as_omitted=True,
                    repeated=repeated,
                )
            )
            logger.info(
                "Added %s as ommitted entry for %s" % (
                    self._diffs_by_shots[shot_name][-1].cut_item_name,
                    shot_name,
                )
            )
        self._recompute_counts()
        if leftover_shots:
            # This shouldn't happen, as our list of Shots comes from edits
            # and CutItems, and we should have processed all of them. Issue
            # a warning if it is the case.
            logger.warning("Found %s left over Shots..." % leftover_shots)

    @property
    def sg_link(self):
        """
        Return the SG Entity the previous Cut was linked to.

        :returns: A SG Entity dictionary, or ``None``.
        """
        return self._sg_entity

    @property
    def diffs_by_shots(self):
        """
        Return the :class:`SGCutDiffGroup` grouped by Shots.

        :returns: A dictionary where keys are Shot names and values :class:`SGCutDiffGroup`
                  instances.
        """
        return self._diffs_by_shots

    @classmethod
    def old_clip_for_shot(cls, for_clip, prev_clip_list, sg_shot, sg_version=None):
        """
        Return a Clip for the given Clip and Shot from the given list of Clip list.

        The prev_clip_list list is modified inside this method, entries being
        removed as they are chosen.

        Best matching Clip is returned, a score is computed for each entry
        from:
        - Is it linked to the right Shot?
        - Is it linked to the right Version?
        - Is the index the same?
        - Is the tc in the same?
        - Is the tc out the same?

        :param for_clip: A Clip instance.
        :param prev_clip_list: A list of Clip instances to consider.
        :param sg_shot: A SG Shot dictionary.
        :param sg_version: A SG Version dictionary.
        :returns: A Clip, or ``None``.
        """

        potential_matches = []
        for clip in prev_clip_list:
            sg_cut_item = clip.metadata.get("sg")
            # Is it linked to the given Shot ?
            if (
                sg_cut_item
                and sg_cut_item["shot"]
                and sg_cut_item["shot"]["id"] == sg_shot["id"]
                and sg_cut_item["shot"]["type"] == sg_shot["type"]
            ):
                # We can have multiple CutItems for the same Shot
                # use the linked Version to pick the right one, if
                # available
                if not sg_version:
                    # No particular Version to match, score is based on
                    # on differences between Cut order, tc in and out
                    # give score a bonus as we don't have an explicit mismatch
                    potential_matches.append((
                        clip,
                        100 + cls._get_matching_score(clip, for_clip)
                    ))
                elif sg_cut_item["version"]:
                    if sg_version["id"] == sg_cut_item["version"]["id"]:
                        # Give a bonus to score as we matched the right
                        # Version
                        potential_matches.append((
                            clip,
                            1000 + cls._get_matching_score(clip, for_clip)
                        ))
                    else:
                        # Version mismatch, don't give any bonus
                        potential_matches.append((
                            clip,
                            cls._get_matching_score(clip, for_clip)
                        ))
                else:
                    # Will keep looking around but we keep a reference to
                    # CutItem since it is linked to the same Shot
                    # give score a little bonus as we didn't have any explicit
                    # mismatch
                    potential_matches.append((
                        clip,
                        100 + cls._get_matching_score(clip, for_clip)
                    ))
            else:
                logger.debug("Rejecting %s for %s" % (clip.cut_item_name, for_clip.cut_item_name))
        if potential_matches:
            potential_matches.sort(key=lambda x: x[1], reverse=True)
            for pm in potential_matches:
                logger.debug("Potential matches %s score %s" % (
                    pm[0].cut_item_name, pm[1],
                ))
            # Return just the CutItem, not including the score
            best = potential_matches[0][0]
            # Prevent this one to be matched multiple times
            prev_clip_list.remove(best)
            logger.debug("Best is %s for %s" % (best.cut_item_name, for_clip.cut_item_name))
            return best
        return None

    def count_for_type(self, diff_type):
        """
        Return the number of entries for the given CutDiffType.

        :param diff_type: A CutDiffType.
        :returns: An integer.
        """
        return self._counts.get(diff_type, 0)

    def diffs_for_type(self, diff_type, just_earliest=False):
        """
        Iterate over SGCutDiff instances for the given CutDiffType.

        :param diff_type: A CutDiffType.
        :param just_earliest: Whether or not all matching SGCutDiff should be
                              returned or just the earliest(s).
        :yields: SGCutDiff instances.
        """
        for shot_name, clip_group in self._diffs_by_shots.items():
            if just_earliest:
                cut_diff = clip_group.earliest_clip
                if not cut_diff:
                    raise ValueError(clip_group._clips[0].name)
                if cut_diff.interpreted_diff_type == diff_type:
                    yield cut_diff
            else:
                for cut_diff in clip_group.clips:
                    if cut_diff.interpreted_diff_type == diff_type:
                        yield cut_diff

    def get_report(self, title, sg_links):
        """
        Build a text report for this summary, highlighting changes.

        :param title: A title for the report.
        :param sg_links: Shotgun URLs to display in the report as links.
        :return: A (subject, body) tuple, as strings.
        """
        # Body should look like this:
        # The changes in {Name of Cut/EDL} are as follows:
        #
        # 5 New Shots
        # HT0500
        # HT0510
        # HT0520
        # HT0530
        # HT0540
        #
        # 2 Omitted Shots
        # HT0050
        # HT0060
        #
        # 1 Reinstated Shot
        # HT0110
        #
        # 4 Cut Changes
        # HT0070 - Head extended 2 frs
        # HT0080 - Tail extended 6 frs
        # HT0090 - Tail trimmed 5 frs
        # HT0100 - Head extended 5 frs
        #
        # 1 Rescan Needed
        # HT0120 - Head extended 15 frs

        subject = self.get_summary_title(title)
        # Note: Cut changes were previously reported with sometimes some reasons
        # and some other times no reasons at all. This was confusing for clients.
        # So for now we don't show any reason.
#        cut_changes_details = [
#            "%s - %s" % (
#                edit.name, ", ".join(edit.reasons)
#            ) for edit in sorted(
#                self.diffs_for_type(_DIFF_TYPES.CUT_CHANGE),
#                key=lambda x: x.index
#            )
#        ]
        cut_changes_details = [
            "%s" % (
                diff.name
            ) for diff in sorted(
                self.diffs_for_type(_DIFF_TYPES.CUT_CHANGE),
                key=lambda x: x.index
            )
        ]
        rescan_details = [
            "%s - %s" % (
                diff.name, ", ".join(diff.reasons)
            ) for diff in sorted(
                self.diffs_for_type(_DIFF_TYPES.RESCAN),
                key=lambda x: x.index
            )
        ]
        no_link_details = [
            diff.sg_version_name or str(diff.index) for diff in sorted(
                self.diffs_for_type(_DIFF_TYPES.NO_LINK),
                key=lambda x: x.index
            )
        ]
        body = _BODY_REPORT_FORMAT % (
            # Let the user know that something is potentially wrong
            "WARNING, following edits couldn't be linked to any Shot :\n%s\n" % (
                "\n".join(no_link_details)
            ) if no_link_details else "",
            # Urls
            " , ".join(sg_links),
            # Title
            title,
            # And then counts and lists per type of changes
            self.count_for_type(_DIFF_TYPES.NEW),
            "\n".join([
                diff.shot_name for diff in sorted(
                    self.diffs_for_type(_DIFF_TYPES.NEW, just_earliest=True),
                    key=lambda x: x.index
                )
            ]),
            self.count_for_type(_DIFF_TYPES.OMITTED),
            "\n".join([
                diff.shot_name for diff in sorted(
                    self.diffs_for_type(_DIFF_TYPES.OMITTED, just_earliest=True),
                    key=lambda x: x.index or -1
                )
            ]),
            self.count_for_type(_DIFF_TYPES.REINSTATED),
            "\n".join([
                diff.shot_name for diff in sorted(
                    self.diffs_for_type(_DIFF_TYPES.REINSTATED, just_earliest=True),
                    key=lambda x: x.index
                )
            ]),
            self.count_for_type(_DIFF_TYPES.CUT_CHANGE),
            "\n".join(cut_changes_details),
            self.count_for_type(_DIFF_TYPES.RESCAN),
            "\n".join(rescan_details),
        )
        return subject, body

    def get_summary_title(self, subject):
        """
        Return a string suitable as a title for Cut changes reports.

        :param str subject: A string, usually a SG Cut name.
        """
        if self._sg_entity:
            return "%s Cut Summary changes on %s" % (
                self._sg_entity["type"].title(),
                subject
            )
        return "Cut Summary for %s" % subject

    def get_diffs_by_change_type(self):
        """
        Returns a dictionary with lists of CutDiffs grouped by cut change type.

        :returns: A dictionary where keys are cut change types and values are sorted
                  list of :class:`CutDiff` instances.
        """
        diff_groups = {}
        diff_groups[_DIFF_TYPES.CUT_CHANGE] = sorted(
            self.diffs_for_type(_DIFF_TYPES.CUT_CHANGE),
            key=lambda x: x.index
        )
        diff_groups[_DIFF_TYPES.RESCAN] = sorted(
            self.diffs_for_type(_DIFF_TYPES.RESCAN),
            key=lambda x: x.index
        )
        diff_groups[_DIFF_TYPES.NO_LINK] = sorted(
            self.diffs_for_type(_DIFF_TYPES.NO_LINK),
            key=lambda x: x.index
        )
        diff_groups[_DIFF_TYPES.NEW] = sorted(
            self.diffs_for_type(_DIFF_TYPES.NEW, just_earliest=True),
            key=lambda x: x.index
        )
        diff_groups[_DIFF_TYPES.OMITTED] = sorted(
            self.diffs_for_type(_DIFF_TYPES.OMITTED, just_earliest=True),
            key=lambda x: x.old_index or -1
        )
        diff_groups[_DIFF_TYPES.REINSTATED] = sorted(
            self.diffs_for_type(_DIFF_TYPES.REINSTATED, just_earliest=True),
            key=lambda x: x.index
        )
        return diff_groups

    @classmethod
    def _get_matching_score(cls, clip_a, clip_b):
        """
        Return a matching score for the given two clips, based on:
        - Is the Cut order the same?
        - Is the tc in the same?
        - Is the tc out the same?

        So the best score is 3 if all of them match

        :param clip_a: a Clip.
        :param clip_b: a Clip.
        :returns: A score, as an integer
        """
        score = 0
        # Compute the Cut order difference (edit.id is the Cut order in an EDL)
        diff = clip_a.index - clip_b.index
        if diff == 0:
            score += 1
        diff = (clip_a.source_in - clip_b.source_in).to_frames()
        if diff == 0:
            score += 1
        diff = (clip_a.source_out - clip_b.source_out).to_frames()
        if diff == 0:
            score += 1

        return score

    def _recompute_counts(self):
        """
        Recompute internal counts from Cut differences
        """
        # Use a defaultdict so we don't have to worry about key existence
        self._counts = defaultdict(int)
        self._total_count = 0
        for shot_name, clip_group in self._diffs_by_shots.items():
            _, _, _, _, _, _, shot_diff_type = clip_group.get_shot_values()
            if shot_diff_type in _PER_SHOT_TYPE_COUNTS:
                # We count these per shots
                self._counts[shot_diff_type] += 1
                # We don't want to include omitted entries in our total
                if shot_diff_type != _DIFF_TYPES.OMITTED:
                    self._total_count += 1
            else:
                # We count others per entries
                for cut_diff in clip_group:
                    # We don't use cut_diff.interpreted_type here, as it will
                    # loop over all siblings, repeated shots cases are handled
                    # with the shot_diff_type
                    diff_type = self._interpreted_diff_type(cut_diff.diff_type)
                    self._counts[diff_type] += 1
                    # We don't want to include omitted entries in our total
                    if cut_diff.diff_type not in [
                        _DIFF_TYPES.OMITTED_IN_CUT,
                        _DIFF_TYPES.OMITTED
                    ]:
                        self._total_count += 1
        logger.debug("%s" % self._counts)

    def _get_shot_link_field(self, sg_entity_type):
        """

        :returns: A SG Shot field name.
        """
        # Retrieve a "link" field on Shots which accepts our Entity type
        shot_schema = self._sg.schema_field_read("Shot")
        # Prefer a sg_<entity type> field if available
        type_display_name = get_entity_type_display_name(
            self._sg,
            sg_entity_type,
        )
        field_name = "sg_%s" % type_display_name.lower()
        field = shot_schema.get(field_name)
        if (
            field
            and field["data_type"]["value"] == "entity"
            and sg_entity_type in field["properties"]["valid_types"]["value"]
        ):
            logger.debug("Found preferred Shot field %s" % field_name)
            return field_name

        # General lookup
        for field_name, field in shot_schema.items():
            # the field has to accept entities and be editable.
            if field["data_type"]["value"] == "entity" and field["editable"]["value"]:
                if sg_entity_type in field["properties"]["valid_types"]["value"]:
                    logger.debug("Found field %s to link %s to shots" % (
                        field_name,
                        sg_entity_type
                    ))
                    return field_name

        logger.warning(
            "Couldn't retrieve a SG Shot field accepting %s" % (
                self._sg_entity_type,
            )
        )
        return None

    def _interpreted_diff_type(self, diff_type):
        """
        Some difference types are grouped under a common type, return
        this group type for the given difference type

        :returns: A _DIFF_TYPES
        """
        if diff_type in [_DIFF_TYPES.NEW_IN_CUT, _DIFF_TYPES.OMITTED_IN_CUT]:
            return _DIFF_TYPES.CUT_CHANGE
        return diff_type

    def __len__(self):
        """
        Return the total number of :class:`SGCutDiff` entries in this SGTrackDiff.

        :returns: An integer.
        """
        return sum([len(self._diffs_by_shots[k]) for k in self._diffs_by_shots], 0)

    def __iter__(self):
        """
        Iterate over Shots for this SGTrackDiff.

        :yields: Shot names, as strings.
        """
        for name in self._diffs_by_shots.keys():
            yield name

    def __getitem__(self, key):
        """
        Return the :class:`SGCutDiffGroup` for a given Shot name.

        :param str key: A Shot name or ``None``.
        :returns: A list of :class:`SGCutDiff` instances or ``None``.
        """
        if key:
            return self._diffs_by_shots.get(key.lower())
        return self._diffs_by_shots.get(key)

    def iteritems(self):
        """
        Iterate over Shot names for this SGTrackDiff, yielding (name, :class:`SGCutDiffGroup`)
        tuples.

        :yields: (name, :class:`SGCutDiffGroup`) tuples.
        """
        for name, item in self._diffs_by_shots.items():
            yield (name, item)

    # Follow Python3 iterators changes and provide an items method iterating
    # other the items
    items = iteritems
