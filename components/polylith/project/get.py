from collections.abc import Generator
from pathlib import Path

import tomlkit
from polylith.repo import default_toml


def get_project_package_includes(data) -> list[dict]:
    return data["tool"]["poetry"]["packages"]


def get_project_name(data) -> str:
    return data["tool"]["poetry"]["name"]


def get_toml(root: Path) -> tomlkit.TOMLDocument:
    with root.open() as f:
        return tomlkit.loads(f.read())


def get_project_files(root: Path) -> Generator:
    return root.glob(f"projects/**/{default_toml}")


def get_project_names(root: Path) -> list[str]:
    file_paths = get_project_files(root)
    tomls = (get_toml(p) for p in file_paths)

    return [get_project_name(d) for d in tomls]
