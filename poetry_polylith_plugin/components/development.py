from pathlib import Path

from poetry_polylith_plugin.components.dirs import create_dir


def create_development(path: Path, keep=True):
    create_dir(path, "development/src/dev", keep=keep)
