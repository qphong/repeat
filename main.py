from manager import Manager

import os
import constants
import util
import files

import argparse

parser = argparse.ArgumentParser(
    prog="Repeat",
    description="Vy learns a subject with spaced-repetition",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

parser.add_argument(
    "-c",
    "--command",
    choices=[
        "add_subject",  # subject
        "list_subjects",
        "list",  # subject, states, tags, by, direction
        "add",  # subject, identifier, name, tags
        "remove",  # subject, identifier
        "get_file",  # subject, identifier, postifx
        "get_files_by_tag",  # subject, tags, postifx
        "get_name",  # subject, identifier
        "get_tags_by_identifier",  # subject, identifier
        "get_new_tags_to_identifier",  # subject, identifier
        "list_file",  # list all postfix # subject, identifier
        "review",  # subject, tags, k
        "add_tag",  # subject, identifier, tags
        "remove_tag",  # subject, identifier, tags
        "start",  # subject, identifier
        "end",  # subject, identifier, passfail
        "cancel",  # subject, identifier
        "list_tag",  # subject
        "list_state",  # subject, tags
        "list_state_by_tag",  # subject, tags
    ],
    type=str,
    required=True,
)

parser.add_argument("--subject", type=str, help="subject identifier")

parser.add_argument(
    "-i", "--identifier", type=str, help="item identifier", default=constants.AUTO_ID
)
parser.add_argument("-n", "--name", type=str, help="item name")
parser.add_argument(
    "-r",
    "--passfail",
    choices=[constants.PASS, constants.FAIL],
    type=str,
    help="result",
)

parser.add_argument(
    "-t", "--tags", type=str, help="tags separated by comma", default=None
)  # comma separated

parser.add_argument(
    "-a",
    "--states",
    type=str,
    # choices=constants.STATES,
    help="states separated by comma",
    default=None,
)  # comma separated
parser.add_argument(
    "-b",
    "--by",
    type=str,
    choices=list(constants.BY_TO_PROPERTY.keys()),
    default="view",
)
parser.add_argument(
    "-d", "--direction", type=str, choices=["inc", "dec"], default="inc"
)
parser.add_argument("-p", "--postfix", type=str, default="untitled.txt")

args = parser.parse_args()
config = vars(args)


command = config["command"]

if command == "add_subject":
    # add a new subject, create all necessary directories and files
    subject = util.parse_args(config, ["subject"], [True])
    files.makedirs_for_subject(subject)

elif command == "list_subjects":
    subjects = files.list_all_subjects()
    print(subjects)

elif command == "add":
    # subject, identifier, name, tags
    subject, identifier, name, tags = util.parse_args(
        config, ["subject", "identifier", "name", "tags"], [True, False, True, False]
    )

    manager = Manager(subject)
    manager.load()
    manager.add(identifier, tags, {"name": name})
    manager.save()

elif command == "remove":
    # subject, identifier
    subject, identifier = util.parse_args(
        config, ["subject", "identifier"], [True, True]
    )

    manager = Manager(subject)
    manager.load()
    manager.remove_item_by_identifier(identifier)
    manager.save()

elif command == "list":
    # subject, states, tags, by, direction
    subject, states, tags, by, direction = util.parse_args(
        config,
        ["subject", "states", "tags", "by", "direction"],
        [True, False, False, False, False],
    )
    manager = Manager(subject)
    manager.load()

    identifiers = manager.get_identifiers_by_states_and_tags(tags, states)
    info_list = manager.get_item_by_identifiers(identifiers)

    info_property = constants.BY_TO_PROPERTY[by]
    sorted_info_list = []
    for i, info_dict in enumerate(info_list):
        sorted_info_list.append((info_dict[info_property], i, info_dict))

    sorted_info_list = sorted(sorted_info_list)
    if direction == "dec":
        sorted_info_list = sorted_info_list[::-1]

    for _, _, info_dict in sorted_info_list:
        readable_info = util.get_readable_info(
            info_dict,
            content_fields=["name"],
            extra_info=constants.BY_TO_INFO_SHOW[by]["show"],
            emphasis=constants.BY_TO_INFO_SHOW[by]["emphasis"],
        )
        print(readable_info)

elif command == "get_file":
    # subject, identifier, postifx
    subject, identifier, postfix = util.parse_args(
        config, ["subject", "identifier", "postfix"], [True, True, True]
    )
    manager = Manager(subject)
    manager.load()
    content = manager.get_content_by_identifier(identifier)
    if not content:
        print("##_not_exist_##")
        exit(1)

    name = "unnamed"
    if "name" in content:
        name = content["name"]

    print(files.get_study_file(subject, identifier, postfix, name))

elif command == "get_files_by_tag":
    # subject, tag, postifx
    subject, tags, postfix = util.parse_args(
        config, ["subject", "tags", "postfix"], [True, True, True]
    )
    manager = Manager(subject)
    manager.load()
    identifiers = manager.get_identifiers_by_tags(tags)

    for identifier in identifiers:
        content = manager.get_content_by_identifier(identifier)
        if not content or "name" not in content:
            continue
        filepath = files.get_study_file(subject, identifier, postfix, content["name"])
        if os.path.isfile(filepath):
            print(filepath)


elif command == "get_name":
    # subject, identifier
    subject, identifier = util.parse_args(
        config, ["subject", "identifier"], [True, True, True]
    )
    manager = Manager(subject)
    manager.load()
    content = manager.get_content_by_identifier(identifier)
    if not content:
        print("##_not_exist_##")
        exit(1)

    name = "unnamed"
    if "name" in content:
        name = content["name"]
    print(name)

elif command == "get_tags_by_identifier":
    subject, identifier = util.parse_args(
        config, ["subject", "identifier"], [True, True]
    )
    manager = Manager(subject)
    manager.load()
    tags = manager.get_tags_by_identifier(identifier)
    if not tags:
        print(f"Cannot find any tag from {identifier}")
        exit(1)

    for tag in sorted(tags):
        print(tag)

elif command == "get_new_tags_to_identifier":  # subject, identifier
    subject, identifier = util.parse_args(
        config, ["subject", "identifier"], [True, True]
    )
    manager = Manager(subject)
    manager.load()
    tags = manager.get_tags_by_identifier(identifier)
    new_tags = list(manager.tags.difference(tags))

    if not new_tags:
        print(f"Cannot find any tag from {identifier}")
        exit(1)

    for tag in sorted(new_tags):
        print(tag)

elif command == "list_file":
    # list all postfix # subject, identifier
    subject, identifier = util.parse_args(
        config, ["subject", "identifier"], [True, True]
    )
    for file in files.list_all_study_files(subject, identifier):
        print(file)

elif command == "review":
    # subject, tags, k
    subject, tags, by = util.parse_args(
        config, ["subject", "tags", "by"], [True, False, True]
    )
    manager = Manager(subject)
    manager.load()
    identifiers = manager.suggest(
        constants.DEFAULT_NUMBER_OF_SUGGESTION[by], tags, by=by
    )

    info_list = manager.get_item_by_identifiers(identifiers)

    for info_dict in info_list:
        readable_info = util.get_readable_info(
            info_dict,
            content_fields=["name"],
            extra_info=[
                constants.LABEL_CONTENT,
                constants.LABEL_TAG,
                constants.LABEL_STATE,
                constants.LABEL_COMPETENCY,
                constants.LABEL_PASS_PCT,
            ],
        )
        print(readable_info)

elif command == "add_tag":
    # subject, identifier, tags
    subject, identifier, tags = util.parse_args(
        config, ["subject", "identifier", "tags"], [True, True, True]
    )
    if len(tags) == 0:
        print("No tag provided!")
        exit(1)

    manager = Manager(subject)
    manager.load()
    manager.add_tags_to_identifier(identifier, tags)
    manager.save()

elif command == "remove_tag":
    # subject, identifier, tags
    subject, identifier, tags = util.parse_args(
        config, ["subject", "identifier", "tags"], [True, True, True]
    )
    if len(tags) == 0:
        print("No tag provided!")
        exit(1)

    manager = Manager(subject)
    manager.load()
    manager.remove_tags_from_identifier(identifier, tags)
    manager.save()

elif command == "start":
    # subject, identifier
    subject, identifier = util.parse_args(
        config, ["subject", "identifier"], [True, True]
    )
    manager = Manager(subject)
    manager.load()
    manager.start_study_item(identifier)
    manager.save()

elif command == "end":
    # subject, identifier, passfail
    subject, identifier, passfail = util.parse_args(
        config, ["subject", "identifier", "passfail"], [True, True, True]
    )
    manager = Manager(subject)
    manager.load()
    manager.end_study_item(identifier, passfail)
    manager.save()

elif command == "cancel":
    subject, identifier = util.parse_args(
        config, ["subject", "identifier"], [True, True]
    )
    manager = Manager(subject)
    manager.load()
    manager.cancel_study_item(identifier)
    manager.save()

elif command == "list_tag":
    # subject
    subject, states = util.parse_args(config, ["subject", "states"], [True, False])
    manager = Manager(subject)
    manager.load()
    tag_count = manager.list_tags(states)
    for tag, count in tag_count:
        print(f"{tag:20s}: {count:>4d}")

elif command == "list_state":
    # subject, tags
    subject, tags = util.parse_args(config, ["subject", "tags"], [True, False])
    manager = Manager(subject)
    manager.load()
    state_count = manager.list_states(tags)
    for state, count in state_count:
        print(f"{state}: {count}")

elif command == "list_state_by_tag":
    # subject, states
    subject, states = util.parse_args(config, ["subject", "states"], [True])
    manager = Manager(subject)
    manager.load()

    tag_count = manager.list_tags(states)

    for tag, count in tag_count:
        print(f"{tag:20s} : {count:>4d}", end="")

        state_count = manager.list_states([tag], states)
        display_state = False
        for state, scount in state_count:
            if state != constants.STATE_STUDIED:
                styled_state = constants.GET_STYLED_STATE(state)

                if not display_state:
                    print(":", end="")
                print(f"{styled_state}({scount})", end=" ")
                display_state = True
        print("")

else:
    raise Exception(f"Unknown command: {command}")
