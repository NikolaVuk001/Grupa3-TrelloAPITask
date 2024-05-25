from os import makedirs, path


def ensure_directory_exists(dir: str):
    if not path.exists(dir):
        makedirs(dir)
