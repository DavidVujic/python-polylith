from pathlib import Path

from polylith.dirs import create_dir


def create_development(path: Path, keep=True) -> None:
    create_dir(path, "development", keep=keep)
