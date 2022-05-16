from pathlib import Path


def create_file(path):
    working_file = Path(path)
    working_file.parent.mkdir(exist_ok=True)
    working_file.touch(exist_ok=True)

    return working_file
