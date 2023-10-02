import math

SECS_MIN = lambda MIN: 60.0 * MIN
SECS_HOUR = lambda HOUR: 3600.0 * HOUR
SECS_DAY = lambda DAY: 3600.0 * 24.0 * DAY
INF = 1e16
PASS = "pass"
FAIL = "fail"

AUTO_ID = "##_AUTO_GENERATE_##"

TRACKER_DEFAULT_INTERVAL = SECS_DAY(1)
TRACKER_DEFAULT_OLDEST_EPOCH = SECS_DAY(60)

DEFAULT_NEXT_BOX_PROBABILITY = 1.0 - 0.8

STATE_STUDYING = "studying"
STATE_NEW = "new"
STATE_STUDIED = "studied"
STATES = [STATE_STUDYING, STATE_NEW, STATE_STUDIED]

INVALID_DURATION = -1

DEFAULT_BOX_TRANSFORMATION = lambda at_time, box: box + 1.0 * math.exp(-at_time)

LABEL_COMPETENCY = "competency"
LABEL_TAG = "tag"
LABEL_STATE = "state"
LABEL_PASS_PCT = "pass_percentage"
LABEL_DURATION = "duration"
EXTRA_INFO = [LABEL_TAG, LABEL_STATE, LABEL_COMPETENCY, LABEL_PASS_PCT, LABEL_DURATION]

DEFAULT_NUMBER_OF_SUGGESTION = 1


BY_TO_PROPERTY = {
    "pass": "n_pass",  # total n_pass
    "competency": "competency",  # time-aware box
    "view": "n_study",  # n_study
    "recent": "since_last_start_study",  # since last start
    "duration": "duration",  # total duration
}


STYLE_HEADER = '\033[95m'
STYLE_OKBLUE = '\033[94m'
STYLE_OKCYAN = '\033[96m'
STYLE_OKGREEN = '\033[92m'
STYLE_WARNING = '\033[93m'
STYLE_FAIL = '\033[91m'
STYLE_BOLD = '\033[1m'
STYLE_UNDERLINE = '\033[4m'
STYLE_ENDC = '\033[0m'

