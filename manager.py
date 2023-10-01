import os
from collections import defaultdict
import json
import random

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

    def remove_tags(self, identifiers, tags):
        for tag in tags:
            self.identifier_by_tag[tag].remove(identifier)

            if len(self.identifier_by_tag[tag]) == 0:
                del self.identifier_by_tag[tag]
                self.tags.remove(tag)

    def add_tags(self, identifier, tags):
        for tag in tags:
            self.tags.add(tag)
            self.identifier_by_tag[tag].add(identifier)

    def list_tags(self):
        return [(tag, len(ids)) for tag, ids in self.identifier_by_tag.items()]

    def list_states(self, tags):
        identifiers = self.get_identifiers_by_tags(tags)
        state_count = defaultdict(int)

        for identifier in identifiers:
            item_tracker = self.item_tracker_data[identifier]
            tracker = item_tracker["tracker"]
            state = tracker.get_state()
            state_count[state] += 1

        return list(state_count.items())

    def add(self, identifier, tags, content):
        if identifier == constants.AUTO_ID:
            # automatically generate a unique item identifier
            identifier = util.get_random_string()
            while identifier in self.item_tracker_data:
                identifier = util.get_random_string()
            print(f"Randomly generate identifier: {identifier}.")

        elif identifier in self.item_tracker_data:
            print(f"{item.identifier} already exists!")
            return 1

        item = Item(identifier, tags, content)
        tracker = Tracker(
            identifier,
            interval=constants.TRACKER_DEFAULT_INTERVAL,
            oldest_epoch=constants.TRACKER_DEFAULT_OLDEST_EPOCH,
        )

        self.item_tracker_data[identifier] = {"item": item, "tracker": tracker}
        self.add_tags(identifier, tags)

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

        return self.get_identifiers_by_tags(
            tags, identifiers
        )

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
        next_box_prob=constants.DEFAULT_NEXT_BOX_PROBABILITY,
    ):
        within_identifiers = self.get_identifiers_by_states_and_tags(tags)

        # get list of min_box from all items
        assessing_boxes = defaultdict(list)  # box -> list of identifiers
        for identifier in within_identifiers:
            tracker = self.item_tracker_data[identifier]["tracker"]

            if tracker.is_studied():
                box = tracker.get_assessing_box(
                    transformation=constants.DEFAULT_BOX_TRANSFORMATION
                )
                assessing_boxes[box].append(identifier)

        if len(assessing_boxes) == 0:
            return []

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
