from pathlib import Path


def create_file(path: Path, name: str) -> Path:
    fullpath = path / name

    fullpath.touch()

    return fullpath
