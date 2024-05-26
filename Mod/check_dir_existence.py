from os import makedirs, path


def ensure_directory_exists(directory: str):
    if not path.exists(directory):
        makedirs(directory)
