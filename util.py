import random
import math
import datetime
import constants


def get_random_string():
    return f"{random.getrandbits(20)}"


def get_now_epoch():
    return (datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds()


def parse_args(config, arguments, required):
    results = []

    for i, argument in enumerate(arguments):
        if argument in [
            "command",
            "subject",
            "identifier",
            "name",
            "by",
            "direction",
            "postfix",
            "passfail",
        ]:
            if required[i] and (
                config[argument] == None or config[argument] == constants.AUTO_ID
            ):
                raise Exception(f"Require {argument}")

            results.append(config[argument])

        elif argument in ["tags", "states"]:
            if config[argument] is None or config[argument] == "all":
                results.append([])
            else:
                results.append(
                    [
                        elem.strip()
                        for elem in config[argument].split(",")
                        if len(elem.strip()) > 0
                    ]
                )

        else:
            raise Exception(f"Unknown argument: {argument}")

    if len(results) == 1:
        return results[0]
    return results


def get_info(identifier, item, tracker):
    state = tracker.get_state()
    box = tracker.get_assessing_box(transformation=constants.DEFAULT_BOX_TRANSFORMATION)
    n_pass = tracker.get_overall_n_pass()
    n_fail = tracker.get_overall_n_fail()
    n_study = n_pass + n_fail
    duration = tracker.get_overall_duration()

    info = {
        "identifier": identifier,
        "content": item.content,
        "tags": list(item.tags),
        "state": state,
        "competency": box,
        "n_pass": n_pass,
        "n_fail": n_fail,
        "n_study": n_study,
        "pass_pct": float(n_pass) / n_study if n_study > 0 else 0.0,
        "duration": duration,
    }

    since_last_end_study = tracker.get_duration_since_last_end_study()

    if state == constants.STATE_NEW:
        info["since_last_start_study"] = constants.INF
    else:
        info["since_last_start_study"] = tracker.get_duration_since_last_start_study()

    if state == constants.STATE_NEW:
        info["since_last_end_study"] = constants.INF
    else:
        info["since_last_end_study"] = tracker.get_duration_since_last_end_study()

    return info


def get_readable_tag(tag, style=False):
    if not style or tag not in constants.TAG_STYLE:
        return tag

    return constants.TAG_STYLE[tag]


def get_readable_state(state, style=False):
    if not style or state not in constants.STATE_STYLE:
        return state

    return constants.STATE_STYLE[state]


def get_readable_info(
    info_dict,
    content_fields,
    extra_info=[
        constants.LABEL_TAG,
        constants.LABEL_STATE,
        constants.LABEL_COMPETENCY,
        constants.LABEL_PASS_PCT,
        constants.LABEL_DURATION,
    ],
    emphasis=[],
):
    info_to_func = {
        constants.LABEL_CONTENT: lambda info_dict, emphasis: show_content(
            info_dict, content_fields, emphasis
        ),
        constants.LABEL_STATE: show_state,
        constants.LABEL_SINCE: show_since,
        constants.LABEL_PASS_PCT: show_passpct,
        constants.LABEL_DURATION: show_duration,
        constants.LABEL_TAG: show_tag,
        constants.LABEL_COMPETENCY: show_competency,
    }

    # info_dict is returned from get_info function
    string = f"[{info_dict['identifier']:6s}]"

    for info in extra_info:
        string += f" {info_to_func[info](info_dict, info in emphasis)}"

    return string


def show_content(info_dict, fields, emphasis=False):
    string = '"'

    for i, field in enumerate(fields):
        string += f"{info_dict['content'][field]}"
        if i > 0:
            string += "|"

    string += '"'

    return string


def show_state(info_dict, emphasis=False):
    state_str = ""

    if info_dict["state"] != constants.STATE_STUDIED:
        state_str = get_readable_state(info_dict["state"], style=True)

    if emphasis:
        return constants.BOLD_TEXT(state_str)
    return state_str


def show_since(info_dict, emphasis=False):
    since_str = ""

    if (
        "since_last_start_study" in info_dict
        and info_dict["since_last_start_study"] < constants.INF
    ):
        since_str = f"{get_readable_duration(info_dict['since_last_start_study'])} ago"

    elif (
        "since_last_end_study" in info_dict
        and info_dict["since_last_end_study"] < constants.INF
    ):
        since_str = f"{get_readable_duration(info_dict['since_last_end_study'])} ago"

    if emphasis:
        return f"{constants.BOLD_TEXT(since_str):<11s}"
    return f"{constants.UNDERLINE_TEXT(since_str):<11s}"


def show_passpct(info_dict, emphasis=False):
    pass_str = ""

    # if info_dict["n_study"] > 0:
    # pass_str = f"({info_dict['n_study']}:{info_dict['n_pass'] / info_dict['n_study'] * 100:.0f}%P)"
    # pass_str = f"{info_dict['n_pass']:3d}/{info_dict['n_study']:<3d}"

    pass_str = f"{info_dict['n_pass']:3d}/{info_dict['n_study']:<3d}"

    if emphasis:
        return constants.BOLD_TEXT(pass_str)
    return pass_str


def show_duration(info_dict, emphasis=False):
    study_duration_str = ""

    if info_dict["duration"] > 0:
        study_duration_str = f"in {get_readable_duration(info_dict['duration']):<7s}"

    if emphasis:
        return constants.BOLD_TEXT(study_duration_str)
    return study_duration_str


def show_tag(info_dict, emphasis=False):
    string = ":"
    sorted_tag = sorted(info_dict["tags"])
    for i, tag in enumerate(sorted_tag):
        tag_str = get_readable_tag(tag, style=True)
        string += tag_str + (":" if i < len(info_dict["tags"]) - 1 else "")
    string += ":"

    if emphasis:
        return constants.BOLD_TEXT(string)
    return string


def show_competency(info_dict, emphasis=False):
    competency_str = f"B:{int(info_dict['competency']):<2d}"

    if emphasis:
        return constants.BOLD_TEXT(competency_str)
    return competency_str


def get_readable_duration(duration):
    if duration == constants.INVALID_DURATION:
        return "INVALID_DURATION"

    tmp = duration / 24 / 60 / 60 / 30
    month = math.floor(tmp)
    tmp = (tmp - month) * 30
    day = math.floor(tmp)
    tmp = (tmp - day) * 24
    hour = math.floor(tmp)
    tmp = (tmp - hour) * 60
    minute = math.floor(tmp)
    second = math.floor((tmp - minute) * 60)
    duration_str = ""

    month_str = f"{month} {'months' if month > 1 else 'month'}"
    day_str = f"{day} {'days' if day > 1 else 'day'}"
    hour_str = f"{hour}h"
    minute_str = f"{minute}m"
    second_str = f"{second}s"

    if month > 0:
        duration_str = f"{month_str}{f' {day_str}' if day > 0 else ''}"
    elif day > 0:
        duration_str = f"{day_str}{f' {hour_str}' if hour > 0 else ''}"
    elif hour > 0:
        duration_str = (
            f"{hour_str if hour > 0 else ''}{minute_str if minute > 0 else ''}"
        )
    else:
        duration_str = (
            f"{minute_str if minute > 0 else ''}{second_str if second > 0 else ''}"
        )
    return duration_str
