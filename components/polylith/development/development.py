from pathlib import Path

from polylith.dirs import create_dir
from polylith.repo import development_dir


def create_development(path: Path, keep=True) -> None:
    create_dir(path, development_dir, keep=keep)
