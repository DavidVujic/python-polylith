from pathlib import Path

from poetry_polylith_plugin.components.projects.constants import dir_name
from poetry_polylith_plugin.components.dirs import create_dir
from poetry_polylith_plugin.components.toml import create_empty_toml


def create_project(path: Path, namespace: str, name: str):
    d = create_dir(path, f"{dir_name}/{name}")

    create_empty_toml(name, d)
