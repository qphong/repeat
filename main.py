from manager import Manager

import constants
import util
import files

import argparse

parser = argparse.ArgumentParser(
    prog="Repeat",
    description="Implementing spaced-repetition",
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
        "get_file",  # subject, identifier, postifx
        "list_file",  # list all postfix # subject, identifier
        "review",  # subject, tags, k
        "start",  # subject, identifier
        "end",  # subject, identifier, passfail
        "cancel", # subject, identifier
        "list_tags",  # subject
        "list_states",  # subject, tags
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
    "-s",
    "--states",
    type=str,
    choices=constants.STATES,
    help="states separated by comma",
    default=None,
)  # comma separated
parser.add_argument(
    "-b",
    "--by",
    type=str,
    choices=[
        "hard",
        "view",
        "recent",
        "duration",
        "pending",
        "new",
        "all",
    ],
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

    for info_dict in info_list:
        readable_info = util.get_readable_info(
            info_dict,
            content_fields=["name"],
            extra_info=[
                constants.LABEL_TAG,
                constants.LABEL_STATE,
                constants.LABEL_COMPETENCY,
                constants.LABEL_PASS_PCT,
            ],
        )
        print(readable_info)

elif command == "get_file":
    # subject, identifier, postifx
    subject, identifier, postfix = util.parse_args(
        config, ["subject", "identifier", "postfix"], [True, True, True]
    )
    print(files.get_study_file(subject, identifier, postfix))

elif command == "list_file":
    # list all postfix # subject, identifier
    subject, identifier = util.parse_args(
        config, ["subject", "identifier"], [True, True]
    )
    for file in files.list_all_study_files(subject, identifier):
        print(file)

elif command == "review":
    # subject, tags, k
    subject, tags = util.parse_args(config, ["subject", "tags"], [True, False])
    manager = Manager(subject)
    manager.load()
    identifiers = manager.suggest(constants.DEFAULT_NUMBER_OF_SUGGESTION, tags)

    info_list = manager.get_item_by_identifiers(identifiers)

    for info_dict in info_list:
        readable_info = util.get_readable_info(
            info_dict,
            content_fields=["name"],
            extra_info=[
                constants.LABEL_TAG,
                constants.LABEL_STATE,
                constants.LABEL_COMPETENCY,
                constants.LABEL_PASS_PCT,
            ],
        )
        print(readable_info)

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

elif command == "list_tags":
    # subject
    subject = util.parse_args(config, ["subject"], [True])
    manager = Manager(subject)
    manager.load()
    tag_count = manager.list_tags()
    for tag, count in tag_count:
        print(f"{tag}: {count}")

elif command == "list_states":
    # subject, tags
    subject, tags = util.parse_args(config, ["subject", "tags"], [True, False])
    manager = Manager(subject)
    manager.load()
    state_count = manager.list_states(tags)
    for state, count in state_count:
        print(f"{state}: {count}")

elif command == "list_state_by_tag":
    subject = util.parse_args(config, ["subject"], [True])
    manager = Manager(subject)
    manager.load()
    tag_count = manager.list_tags()
    for tag, count in tag_count:
        print(f"{tag}: {count} -- ", end="")
        state_count = manager.list_states([tag])
        for state, count in state_count:
            print(f"{state}:{count}", end="  ")
        print("")

else:
    raise Exception(f"Unknown command: {command}")
