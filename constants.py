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
IDENTITY_BOX_TRANSFORMATION = lambda at_time, box: box

LABEL_COMPETENCY = "competency"
LABEL_TAG = "tag"
LABEL_CONTENT = "content"
LABEL_STATE = "state"
LABEL_PASS_PCT = "pass_percentage"
LABEL_SINCE = "since"
LABEL_DURATION = "duration"
EXTRA_INFO = [
    LABEL_CONTENT,
    LABEL_TAG,
    LABEL_STATE,
    LABEL_SINCE,
    LABEL_COMPETENCY,
    LABEL_PASS_PCT,
    LABEL_DURATION,
]

DEFAULT_NUMBER_OF_SUGGESTION = {
    "competency": 1,
    "pass": 1,
    "recent": 1,
    "duration": 1,
}


BY_TO_PROPERTY = {
    "pass": "pass_pct",  # total n_pass
    "competency": "competency",  # time-aware box
    "view": "n_study",  # n_study
    "recent": "since_last_start_study",  # since last start
    "duration": "duration",  # total duration
}

BY_TO_INFO_SHOW = {
    "pass": {
        "show": [
            LABEL_PASS_PCT,
            LABEL_STATE,
            LABEL_CONTENT,
            LABEL_TAG,
            LABEL_SINCE,
        ],
        "emphasis": [LABEL_PASS_PCT],
    },  # total n_pass
    "competency": {
        "show": [
            LABEL_COMPETENCY,
            LABEL_STATE,
            LABEL_CONTENT,
            LABEL_TAG,
            LABEL_SINCE,
        ],
        "emphasis": [LABEL_COMPETENCY],
    },  # time-aware box
    "view": {
        "show": [
            LABEL_PASS_PCT,
            LABEL_STATE,
            LABEL_CONTENT,
            LABEL_TAG,
            LABEL_SINCE,
        ],
        "emphasis": [LABEL_PASS_PCT],
    },  # n_study
    "recent": {
        "show": [
            LABEL_SINCE,
            LABEL_STATE,
            LABEL_CONTENT,
            LABEL_TAG,
            LABEL_PASS_PCT,
        ],
        "emphasis": [LABEL_SINCE],
    },  # since last start
    "duration": {
        "show": [
            LABEL_DURATION,
            LABEL_STATE,
            LABEL_CONTENT,
            LABEL_TAG,
            LABEL_PASS_PCT,
        ],
        "emphasis": [LABEL_DURATION],
    },  # total duration
}


STYLE_HEADER = "\033[95m"
STYLE_OKBLUE = "\033[94m"
STYLE_OKCYAN = "\033[96m"
STYLE_OKGREEN = "\033[92m"
STYLE_WARNING = "\033[93m"
STYLE_FAIL = "\033[91m"
STYLE_BOLD = "\033[1m"
STYLE_UNDERLINE = "\033[4m"
STYLE_ENDC = "\033[0m"

BOLD_TEXT = lambda string: f"{STYLE_BOLD}{string}{STYLE_ENDC}"
UNDERLINE_TEXT = lambda string: f"{STYLE_UNDERLINE}{string}{STYLE_ENDC}"

TAG_STYLE = {
    "E": f"{STYLE_OKGREEN}{STYLE_BOLD}[E]{STYLE_ENDC}",
    "E-": f"{STYLE_OKGREEN}{STYLE_BOLD}[E-]{STYLE_ENDC}",
    "E+": f"{STYLE_OKGREEN}{STYLE_BOLD}[E+]{STYLE_ENDC}",
    "M": f"{STYLE_OKBLUE}{STYLE_BOLD}[M]{STYLE_ENDC}",
    "M+": f"{STYLE_OKBLUE}{STYLE_BOLD}[M+]{STYLE_ENDC}",
    "M-": f"{STYLE_OKBLUE}{STYLE_BOLD}[M-]{STYLE_ENDC}",
    "H": f"{STYLE_FAIL}{STYLE_BOLD}[H]{STYLE_ENDC}",
    "H+": f"{STYLE_FAIL}{STYLE_BOLD}[H+]{STYLE_ENDC}",
    "H-": f"{STYLE_FAIL}{STYLE_BOLD}[H-]{STYLE_ENDC}",
    "vy-todo": f"{STYLE_OKBLUE}vy-todo{STYLE_ENDC}",
    "review": f"{STYLE_FAIL}review{STYLE_ENDC}",
    "refactor": f"{STYLE_OKGREEN}refactor{STYLE_ENDC}",
}

def GET_STYLED_TAG(tag):
    if tag in TAG_STYLE:
        return TAG_STYLE[tag]
    return tag

STATE_STYLE = {
    STATE_NEW: f"{STYLE_WARNING}_new_{STYLE_ENDC}",
    STATE_STUDYING: f"{STYLE_FAIL}_studying_{STYLE_ENDC}",
    STATE_STUDIED: f"{STYLE_FAIL}_studied_{STYLE_ENDC}",
}

def GET_STYLED_STATE(state):
    if state in STATE_STYLE:
        return STATE_STYLE[state]
    return state
