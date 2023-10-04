import sys
import os
from collections import defaultdict
import json
import random
import bisect
import math

import files
import constants
import util

from tracker import Tracker
from item import Item


class Manager:
    def __init__(self, subject):
        self.item_tracker_data = {}  # identifier -> {"item": item, "tracker": tracker}
        self.subject = subject
        self.subject_root = files.get_subject_root(subject)
        self.tags = set()  # set of tags
        self.identifier_by_tag = defaultdict(set)  # tag -> set of item identifiers

    def save(self):
        item_dict = {}
        tracker_dict = {}

        for identifier, item_tracker in self.item_tracker_data.items():
            item_dict[identifier] = item_tracker["item"].to_dictionary()
            tracker_dict[identifier] = item_tracker["tracker"].to_dictionary()

        with open(
            f"{files.get_item_directory(self.subject_root)}/item.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(item_dict, file, indent=2)

        with open(
            f"{files.get_tracker_directory(self.subject_root)}/tracker.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(tracker_dict, file, indent=2)

    def load(self):
        item_path = f"{files.get_item_directory(self.subject_root)}/item.json"
        tracker_path = f"{files.get_tracker_directory(self.subject_root)}/tracker.json"

        item_dict = {}
        tracker_dict = {}

        if os.path.exists(item_path):
            with open(item_path, "r", encoding="utf-8") as file:
                item_dict = json.load(file)
        if os.path.exists(tracker_path):
            with open(tracker_path, "r", encoding="utf-8") as file:
                tracker_dict = json.load(file)

        for identifier in item_dict:
            item = Item.load_from_dictionary(item_dict[identifier])
            tracker = Tracker.load_from_dictionary(tracker_dict[identifier])

            self.item_tracker_data[identifier] = {
                "item": item,
                "tracker": tracker,
            }

            self.add_tags(identifier, item.tags)

    def get_n_item(self):
        return len(self.item_tracker_data)

    def remove_tags_from_identifier(self, identifier, tags):
        if identifier not in self.item_tracker_data:
            print(f"{identifier} does not exist!")
            return 0

        item = self.item_tracker_data[identifier]["item"]
        for tag in tags:
            if tag in item.tags:
                item.tags.remove(tag)
            else:
                print(f"{tag} does not exist in {identifier}!")
                continue

            self.identifier_by_tag[tag].remove(identifier)

            if len(self.identifier_by_tag[tag]) == 0:
                del self.identifier_by_tag[tag]
                self.tags.remove(tag)

    def add_tags_to_identifier(self, identifier, tags):
        if identifier not in self.item_tracker_data:
            print(f"{identifier} does not exists!")
            return 0

        item = self.item_tracker_data[identifier]["item"]
        for tag in tags:
            if tag not in item.tags:
                item.tags.add(tag)
            else:
                print(f"{tag} exists in {identifier}!")
                continue

            self.tags.add(tag)
            self.identifier_by_tag[tag].add(identifier)

    def add_tags(self, identifier, tags):
        # do not modify tags of item
        for tag in tags:
            self.tags.add(tag)
            self.identifier_by_tag[tag].add(identifier)

    def list_tags(self, states=[]):
        if len(states) == 0:
            return sorted(
                [(tag, len(ids)) for tag, ids in self.identifier_by_tag.items()]
            )

        identifiers = self.get_identifiers_by_states(states)
        tag_count = defaultdict(int)

        for identifier in identifiers:
            item_tracker = self.item_tracker_data[identifier]
            item = item_tracker["item"]
            tracker = item_tracker["tracker"]

            if tracker.get_state() in states:
                for tag in item.tags:
                    tag_count[tag] += 1
        return sorted(list(tag_count.items()))

    def list_states(self, tags=[], states=[]):
        identifiers = self.get_identifiers_by_states_and_tags(tags, states)
        state_count = defaultdict(int)

        for identifier in identifiers:
            item_tracker = self.item_tracker_data[identifier]
            tracker = item_tracker["tracker"]
            state = tracker.get_state()
            state_count[state] += 1

        return sorted(list(state_count.items()))

    def add(self, identifier, tags, content):
        if identifier == constants.AUTO_ID:
            # automatically generate a unique item identifier
            identifier = util.get_random_string()
            while identifier in self.item_tracker_data:
                identifier = util.get_random_string()
            print(f"Randomly generate identifier: {identifier}.")

        elif identifier in self.item_tracker_data:
            print(f"{identifier} already exists!")
            return 1

        item = Item(identifier, tags, content)
        tracker = Tracker(
            identifier,
            interval=constants.TRACKER_DEFAULT_INTERVAL,
            oldest_epoch=constants.TRACKER_DEFAULT_OLDEST_EPOCH,
        )

        self.item_tracker_data[identifier] = {"item": item, "tracker": tracker}
        self.add_tags(identifier, tags)

    def get_content_by_identifier(self, identifier):
        if identifier in self.item_tracker_data:
            item = self.item_tracker_data[identifier]["item"]
            return item.content
        return None

    def get_identifiers_by_states(self, states=[], within_identifiers=set()):
        # len(states) == 0 means all all states
        # len(within_identifiers) == 0 means considering all identifiers
        if len(states) == 0:
            if len(within_identifiers) == 0:
                return list(self.item_tracker_data.keys())

            return list(
                set(self.item_tracker_data.keys()).intersection(within_identifiers)
            )

        identifiers = set()
        for identifier, item_tracker in self.item_tracker_data.items():
            if len(within_identifiers) and identifier not in within_identifiers:
                continue

            tracker = item_tracker["tracker"]
            state = tracker.get_state()
            if state in states:
                identifiers.add(identifier)

        return list(identifiers)

    def get_identifiers_by_tags(self, tags=[], within_identifiers=set()):
        # len(tags) == 0 means all tags
        # len(within_identifiers) == 0 means considering all identifiers
        if len(tags) == 0:
            if len(within_identifiers) == 0:
                return list(self.item_tracker_data.keys())

            return list(
                set(self.item_tracker_data.keys()).intersection(within_identifiers)
            )

        identifiers = set()
        for tag in tags:
            identifiers = identifiers.union(self.identifier_by_tag[tag])

        if len(within_identifiers) > 0:
            return list(set(within_identifiers).intersection(identifiers))

        return list(identifiers)

    def get_identifiers_by_states_and_tags(
        self, tags=[], states=[], within_identifiers=set()
    ):
        identifiers = self.get_identifiers_by_states(states, within_identifiers)
        if len(identifiers) == 0:
            return set()

        return self.get_identifiers_by_tags(tags, identifiers)

    def get_item_by_identifiers(self, identifiers):
        item_list = []
        for identifier in identifiers:
            item_tracker = self.item_tracker_data[identifier]

            item = item_tracker["item"]
            tracker = item_tracker["tracker"]

            item_list.append(util.get_info(identifier, item, tracker))

        return item_list

    def start_study_item(self, identifier):
        self.item_tracker_data[identifier]["tracker"].start_study()

    def end_study_item(self, identifier, passfail):
        self.item_tracker_data[identifier]["tracker"].end_study(passfail)

    def cancel_study_item(self, identifier):
        self.item_tracker_data[identifier]["tracker"].cancel_study()

    def suggest(
        self,
        k=1,
        tags=[],
        by="competency",
        next_box_prob=constants.DEFAULT_NEXT_BOX_PROBABILITY,
    ):
        within_identifiers = self.get_identifiers_by_states_and_tags(tags)

        if by == "competency":
            assessing_boxes = self.group_identifiers_by_assessing_box(
                within_identifiers
            )
            if len(assessing_boxes) == 0:
                return []
            return Manager.get_randomized_box(k, assessing_boxes, next_box_prob)

        elif by == "pass":
            unnormalized_probs = [0.0] * len(within_identifiers)

            for i, identifier in enumerate(within_identifiers):
                tracker = self.item_tracker_data[identifier]["tracker"]
                n_pass = tracker.get_overall_n_pass()
                n_study = tracker.get_overall_n_study()

                pass_pct = float(n_pass) / float(n_study) if n_study > 0 else 0.0
                unnormalized_probs[i] = math.exp(-2.5 * pass_pct)

            return Manager.get_randomized_identifier(
                k, within_identifiers, unnormalized_probs
            )

        elif by == "recent":
            unnormalized_probs = [0.0] * len(within_identifiers)

            for i, identifier in enumerate(within_identifiers):
                tracker = self.item_tracker_data[identifier]["tracker"]
                state = tracker.get_state()

                if state == constants.STATE_NEW or state == constants.STATE_STUDYING:
                    unnormalized_probs[i] = 0.0
                else:
                    unnormalized_probs[i] = tracker.get_duration_since_last_end_study()

            return Manager.get_randomized_identifier(
                k, within_identifiers, unnormalized_probs
            )

        elif by == "duration":
            unnormalized_probs = [0.0] * len(within_identifiers)

            for i, identifier in enumerate(within_identifiers):
                tracker = self.item_tracker_data[identifier]["tracker"]
                unnormalized_probs[i] = tracker.get_overall_duration()

            return Manager.get_randomized_identifier(
                k, within_identifiers, unnormalized_probs
            )
        else:
            raise Exception(f"Manager:suggest: Haven't implemented for {by}!")

    def group_identifiers_by_assessing_box(self, identifiers):
        assessing_boxes = defaultdict(list)  # box -> list of identifiers
        for identifier in identifiers:
            tracker = self.item_tracker_data[identifier]["tracker"]

            if tracker.is_studied():
                box = tracker.get_assessing_box(
                    transformation=constants.DEFAULT_BOX_TRANSFORMATION
                )
                assessing_boxes[box].append(identifier)
        return assessing_boxes

    @staticmethod
    def get_randomized_identifier(k, identifiers, unnormalized_probs):
        suggested_identifiers = []

        while len(suggested_identifiers) < k and len(identifiers):
            normalizer = sum(unnormalized_probs)

            cprobs = [0.0] * len(unnormalized_probs)
            cprobs[0] = unnormalized_probs[0] / float(normalizer)
            for i in range(1, len(cprobs)):
                cprobs[i] = cprobs[i - 1] + unnormalized_probs[i] / float(normalizer)

            t = min(random.random(), 1.0 - 1e-9)
            idx = bisect.bisect_left(cprobs, t)

            identifier = identifiers[idx]
            suggested_identifiers.append(identifier)
            identifiers.remove(identifier)
            del unnormalized_probs[idx]

        return suggested_identifiers

    @staticmethod
    def get_randomized_box(k, assessing_boxes, next_box_prob):
        suggested_identifiers = []
        sorted_boxes = sorted(list(assessing_boxes.keys()))

        while len(suggested_identifiers) < k and len(sorted_boxes):
            for i, box in enumerate(sorted_boxes):
                t = random.random()
                if t <= next_box_prob:
                    continue

                idx = random.randint(0, len(assessing_boxes[box]) - 1)
                identifier = assessing_boxes[box][idx]
                suggested_identifiers.append(identifier)

                assessing_boxes[box].remove(identifier)
                if len(assessing_boxes[box]) == 0:
                    sorted_boxes.remove(box)
                break

        return suggested_identifiers
