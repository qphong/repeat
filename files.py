import os
import re
import glob


def get_subject_root_prefix():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return f"{dir_path}/subjects/sbj-"


def list_all_subjects():
    subject_root_prefix = get_subject_root_prefix()
    subjects = []

    for subject_root in glob.glob(f"{subject_root_prefix}*/"):
        subjects.append(subject_root[len(subject_root_prefix) : -1])
    return subjects


def get_study_file_prefix(subject, identifier, text, maxlen):
    text = text[:maxlen]
    study_dir = get_study_directory(get_subject_root(subject))
    if len(text):
        return f"{study_dir}/{identifier}_{text}_"
    return f"{study_dir}/{identifier}_"


def get_study_file(subject, identifier, postfix, text="", maxlen=15):
    text = re.sub(r"\W", "-", text)
    return f"{get_study_file_prefix(subject, identifier, text, maxlen)}{postfix}"


def list_all_study_files(subject, identifier, text="", maxlen=15):
    return glob.glob(f"{get_study_file_prefix(subject, identifier, text, maxlen)}*")


def get_subject_root(subject):
    return f"{get_subject_root_prefix()}{subject}"


def get_manager_meta_data_prefix(subject_root):
    return f"{subject_root}/"


def get_tracker_directory(subject_root):
    return f"{subject_root}/tracker"


def get_item_directory(subject_root):
    return f"{subject_root}/item"


def get_study_directory(subject_root):
    return f"{subject_root}/study"


def get_study_filename(subject_root, filename):
    study_dir = get_study_directory(subject_root)
    return f"{study_dir}/filename"


def makedirs(directories):
    for directory in directories:
        try:
            os.makedirs(directory)
            print(f"Make {directory}")
        except FileExistsError:
            print(f"ERROR: {directory} exists!")


def makedirs_for_subject(subject):
    subject_root = get_subject_root(subject)
    tracker_dir = get_tracker_directory(subject_root)
    item_dir = get_item_directory(subject_root)
    study_dir = get_study_directory(subject_root)

    makedirs([subject_root, tracker_dir, item_dir, study_dir])
