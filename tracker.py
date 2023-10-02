from collections import defaultdict

import util
import constants


class Tracker:
    @staticmethod
    def generate_tracker_data():
        return {
            "n_pass": 0,
            "n_fail": 0,
            "n_study": 0,
            "study_duration": 0.0,
            "box": 0,
        }

    def __init__(
        self,
        identifier,  # use to refer to its content, tags, ...
        interval=constants.SECS_MIN(1),
        oldest_epoch=constants.SECS_DAY(30),
    ):
        """
        0 - interval -> 1 - interval -> 2 - interval -> 3
        """
        self.time_aware_tracker_data = defaultdict(Tracker.generate_tracker_data)

        self.interval = interval
        self.oldest_epoch = oldest_epoch
        self.max_tracker_data_key = int(oldest_epoch / interval)

        self.identifier = identifier

        self.start_study_time = -constants.INF
        self.end_study_time = constants.INF
        self.prev_start_study_time = -constants.INF
        self.prev_end_study_time = constants.INF

    def to_dictionary(self):
        return {
            "identifier": self.identifier,
            "time_aware_tracker_data": dict(self.time_aware_tracker_data),
            "interval": self.interval,
            "oldest_epoch": self.oldest_epoch,
            "max_tracker_data_key": self.max_tracker_data_key,
            "start_study_time": self.start_study_time,
            "end_study_time": self.end_study_time,
            "prev_start_study_time": self.prev_start_study_time,
            "prev_end_study_time": self.prev_end_study_time,
            "state": self.get_state(),
        }

    @staticmethod
    def load_from_dictionary(data_dict):
        tracker = Tracker("dummy_identifier")

        tracker.identifier = data_dict["identifier"]
        tracker.interval = data_dict["interval"]
        tracker.oldest_epoch = data_dict["oldest_epoch"]
        tracker.max_tracker_data_key = int(tracker.oldest_epoch / tracker.interval)
        tracker.start_study_time = data_dict["start_study_time"]
        tracker.end_study_time = data_dict["end_study_time"]
        tracker.prev_start_study_time = data_dict["prev_start_study_time"]
        tracker.prev_end_study_time = data_dict["prev_end_study_time"]

        for key, data in data_dict["time_aware_tracker_data"].items():
            tracker.time_aware_tracker_data[int(key)] = data

        return tracker

    def epoch_to_discrete(self, epoch):
        return int(epoch / self.interval)

    def get_duration_since_last_end_study(self, at_time=None):
        if not at_time:
            at_time = util.get_now_epoch()

        if self.end_study_time < at_time:
            return at_time - self.end_study_time

        return constants.INVALID_DURATION

    def get_duration_since_last_start_study(self, at_time=None):
        if not at_time:
            at_time = util.get_now_epoch()

        return at_time - self.start_study_time

    def get_tracker_data_key(self, at_time=None):
        if not at_time:
            at_time = util.get_now_epoch()

        if self.prev_end_study_time < constants.INF:
            discrete_at_time = self.epoch_to_discrete(at_time)
            discrete_end_study_time = self.epoch_to_discrete(self.prev_end_study_time)

            since_last_study = discrete_at_time - discrete_end_study_time
        else:
            since_last_study = 0

        if since_last_study > self.max_tracker_data_key:
            since_last_study = self.max_tracker_data_key

        return since_last_study

    def get_tracker_data(self, at_time=None):
        key = self.get_tracker_data_key(at_time)
        return self.time_aware_tracker_data[key]

    def start_study(self, at_time=None):
        if self.is_studying():
            print(f"WARNING: {self.identifier} already started studying!")
            return

        if not at_time:
            at_time = util.get_now_epoch()

        self.prev_start_study_time = self.start_study_time
        self.prev_end_study_time = self.end_study_time

        self.start_study_time = at_time
        self.end_study_time = constants.INF

    def get_state(self):
        if self.is_new():
            return constants.STATE_NEW
        if self.is_studying():
            return constants.STATE_STUDYING
        if self.is_studied():
            return constants.STATE_STUDIED
        raise Exception(
            f"Unknown state: start_study_time:{self.start_study_time}, end_study_time: {self.end_study_time}"
        )

    def is_studying(self):
        return self.end_study_time == constants.INF and self.start_study_time > 0

    def is_new(self):
        return (
            self.start_study_time == -constants.INF
            and self.end_study_time == constants.INF
        )

    def is_studied(self):
        return self.end_study_time < constants.INF

    def get_overall_n_study(self):
        n_study = 0
        for tracker in self.time_aware_tracker_data.values():
            n_study += tracker["n_study"]
        return n_study

    def get_overall_n_pass(self):
        n_pass = 0
        for tracker in self.time_aware_tracker_data.values():
            n_pass += tracker["n_pass"]
        return n_pass

    def get_overall_n_fail(self):
        n_fail = 0
        for tracker in self.time_aware_tracker_data.values():
            n_fail += tracker["n_fail"]
        return n_fail

    def get_overall_duration(self):
        duration = 0.0
        for tracker in self.time_aware_tracker_data.values():
            duration += tracker["study_duration"]
        return duration

    def cancel_study(self):
        if self.is_studying():
            self.start_study_time = self.prev_start_study_time
            self.end_study_time = self.prev_end_study_time
        else:
            print("WARNING: cancel_study: nothing to cancel!")

    def end_study(self, status, at_time=None):
        if self.start_study_time == -constants.INF:
            raise Exception(
                "Cannot complete a study that haven't been started studying!"
            )
        if not at_time:
            at_time = util.get_now_epoch()

        if self.start_study_time > at_time:
            raise Exception("end_study: start_study_time > end_study_time!")

        self.end_study_time = at_time

        # update tracker_data
        at_key = self.get_tracker_data_key(at_time)
        tracker_data = self.time_aware_tracker_data[at_key]

        tracker_data["n_study"] += 1
        tracker_data["study_duration"] += self.end_study_time - self.start_study_time

        if status == constants.PASS:
            tracker_data["n_pass"] += 1
            # increase box of self.time_aware_tracker_data[key] to 0 for all key <= at_key by 1
            for key in self.time_aware_tracker_data:
                if key <= at_key:
                    self.time_aware_tracker_data[key]["box"] += 1

        elif status == constants.FAIL:
            tracker_data["n_fail"] += 1
            # reset box of self.time_aware_tracker_data[key] to 0 for all key
            for key in self.time_aware_tracker_data:
                self.time_aware_tracker_data[key]["box"] = 0

        else:
            raise Exception(f"Unknown status: {status}")

    def get_assessing_box(
        self, at_time=None, transformation=constants.DEFAULT_BOX_TRANSFORMATION
    ):
        # to assess memory quality
        if not at_time:
            at_time = util.get_now_epoch()
        at_key = self.get_tracker_data_key(at_time)

        upper_key = at_key
        # lower_key = -1

        if at_key not in self.time_aware_tracker_data:
            for key in self.time_aware_tracker_data:
                if key > at_key:
                    upper_key = min(upper_key, key)
                # else:
                    # lower_key = max(lower_key, key)

            if upper_key in self.time_aware_tracker_data:
                return transformation(
                    at_key, self.time_aware_tracker_data[upper_key]["box"]
                )
            # elif lower_key in self.time_aware_tracker_data:
                # return transformation(
                    # at_key, self.time_aware_tracker_data[lower_key]["box"]
                # )
            else:
                return 0

        return transformation(at_key, self.time_aware_tracker_data[at_key]["box"])
