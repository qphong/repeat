"""
list filtered by tags, state
   sorted by since_last_start_study
          by since_last_end_study

review tags (for completed items by suggesting)

start_study_item
end_study_item: pass, fail
"""

from manager import Manager
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
        "add_task",  # task
        "list_tasks",
        "list",  # task, states, tags, by, direction
        "add",  # task, identifier, name, tags
        "get_file",  # task, identifier, postifx
        "list_file",  # list all postfix # task, identifier
        "review",  # task, tags, k
        "start",  # task, identifier
        "end",  # task, identifier, passfail
        "list_tags",  # task
        "list_states",  # task, tags
    ],
    type=str,
    required=True,
)

parser.add_argument("--task", type=str, help="task identifier")

parser.add_argument("-i", "--identifier", type=str, help="item identifier")
parser.add_argument("-s", "--passfail", type=str)

parser.add_argument(
    "-t", "--tags", type=str, help="tags separated by comma"
)  # comma separated
parser.add_argument(
    "-s", "--states", type=str, help="states separated by comma"
)  # comma separated
parser.add_argument(
    "-b",
    "--by",
    type=str,
    choices=["hard", "view", "recent", "duration", "pending", "new", "all"],
)
parser.add_argument("-d", "--direction", type=str, choices=["inc", "dec"])

args = parser.parse_args()
config = vars(args)


task = config["task"]
command = config["command"]

if command == "add_task":
    # add a new task, create all necessary directories and files
    raise Exception("Haven't implemented!")

elif command == "list_tasks":
    # list all existing tasks and its number of items
    raise Exception("Haven't implemented!")

elif command == "list":
    # task, states, tags, by, direction
    raise Exception("Haven't implemented!")

elif command == "add":
    # task, identifier, name, tags
    raise Exception("Haven't implemented!")

elif command == "get_file":
    # task, identifier, postifx
    raise Exception("Haven't implemented!")

elif command == "list_file":
    # list all postfix # task, identifier
    raise Exception("Haven't implemented!")

elif command == "review":
    # task, tags, k
    raise Exception("Haven't implemented!")

elif command == "start":
    # task, identifier
    raise Exception("Haven't implemented!")

elif command == "end":
    # task, identifier, passfail
    raise Exception("Haven't implemented!")

elif command == "list_tags":
    # task
    raise Exception("Haven't implemented!")

elif command == "list_states":
    # task, tags
    raise Exception("Haven't implemented!")

else:
    raise Exception(f"Unknown command: {command}")

