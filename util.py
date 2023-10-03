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

    info = {
        "identifier": identifier,
        "content": item.content,
        "tags": list(item.tags),
        "state": state,
        "competency": box,
        "n_pass": tracker.get_overall_n_pass(),
        "n_fail": tracker.get_overall_n_fail(),
        "n_study": tracker.get_overall_n_study(),
        "duration": tracker.get_overall_duration(),
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
    if not style:
        return tag

    if tag.startswith("E"):
        return f"{constants.STYLE_OKGREEN}{constants.STYLE_BOLD}{tag}{constants.STYLE_ENDC}"
    elif tag.startswith("M"):
        return (
            f"{constants.STYLE_OKBLUE}{constants.STYLE_BOLD}{tag}{constants.STYLE_ENDC}"
        )
    elif tag.startswith("H"):
        return (
            f"{constants.STYLE_FAIL}{constants.STYLE_BOLD}{tag}{constants.STYLE_ENDC}"
        )

    return tag


def get_readable_state(state, style=False):
    if not style:
        return f"_state_"

    if state == constants.STATE_NEW:
        return f"{constants.STYLE_WARNING}_{constants.STYLE_UNDERLINE}{state}_{constants.STYLE_ENDC}"
    elif state == constants.STATE_STUDYING:
        return f"{constants.STYLE_FAIL}_{constants.STYLE_UNDERLINE}{state}_{constants.STYLE_ENDC}"

    return state


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
    # info_dict is returned from get_info function
    string = f"[{info_dict['identifier']:6s}]"

    for field in content_fields:
        string += f" \"{info_dict['content'][field]}\""

    if constants.LABEL_STATE in extra_info:
        if info_dict["state"] != constants.STATE_STUDIED:
            state_str = get_readable_state(info_dict["state"], style=True)

            string += f" {state_str}"

        if (
            "since_last_start_study" in info_dict
            and info_dict["since_last_start_study"] < constants.INF
        ):
            duration_str = (
                f"({get_readable_duration(info_dict['since_last_start_study'])} ago)"
            )

            if "recent" in emphasis:
                string += f"  {constants.BOLD_TEXT(duration_str)}"
            else:
                string += f"  {duration_str}"

        elif (
            "since_last_end_study" in info_dict
            and info_dict["since_last_end_study"] < constants.INF
        ):
            duration_str = (
                f"({get_readable_duration(info_dict['since_last_end_study'])} ago)"
            )
            if "recent" in emphasis:
                string += f"  {constants.BOLD_TEXT(duration_str)}"
            else:
                string += f"  {duration_str}"

    if constants.LABEL_PASS_PCT in extra_info:
        if info_dict["n_study"] > 0:
            pass_str = f"({info_dict['n_study']}:{info_dict['n_pass'] / info_dict['n_study'] * 100:.0f}%P)"

            if "pass" in emphasis:
                string += f"  {constants.BOLD_TEXT(pass_str)}"
            else:
                string += f"  {pass_str}"

    if constants.LABEL_DURATION in extra_info:
        if info_dict["duration"] > 0:
            study_duration = f"(T:{get_readable_duration(info_dict['duration'])})"

            if "duration" in emphasis:
                string += f"  {constants.BOLD_TEXT(study_duration)}"
            else:
                string += f"  {study_duration}"

    if constants.LABEL_TAG in extra_info:
        string += "  :"
        for i, tag in enumerate(info_dict["tags"]):
            tag_str = get_readable_tag(tag, style=True)
            string += tag_str + (":" if i < len(info_dict["tags"]) - 1 else "")
        string += ":"

    if constants.LABEL_COMPETENCY in extra_info:
        competency_str = f"B:{int(info_dict['competency'])}"

        if "competency" in emphasis:
            string += f"  {constants.BOLD_TEXT(competency_str)}"
        else:
            string += f"  {competency_str}"

    return string


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
