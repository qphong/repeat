import os

def get_task_root(prefix, task):
    return f"{prefix}/task"

def get_tracker_directory(task_root):
    return f"{task_root}/tracker"

def get_item_directory(task_root):
    return f"{task_root}/item"

def get_study_directory(task_root):
    return f"{task_root}/study"

def get_study_filename(task_root, filename):
    study_dir = get_study_directory(task_root)
    return f"{study_dir}/filename"

