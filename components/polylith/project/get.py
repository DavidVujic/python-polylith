from collections.abc import Generator
from pathlib import Path
from typing import List

import tomlkit
from polylith.repo import default_toml


def get_project_package_includes(data) -> List[dict]:
    return data["tool"]["poetry"]["packages"]


def get_project_name(data) -> str:
    return data["tool"]["poetry"]["name"]


def get_toml(root: Path) -> tomlkit.TOMLDocument:
    with root.open() as f:
        return tomlkit.loads(f.read())


def get_project_files(root: Path) -> Generator:
    return root.glob(f"projects/**/{default_toml}")


def get_toml_files(root: Path) -> List[tomlkit.TOMLDocument]:
    project_files = get_project_files(root)

    return [get_toml(p) for p in project_files]


def get_project_names(root: Path) -> List[str]:
    tomls = get_toml_files(root)

    return [get_project_name(d) for d in tomls]


def get_packages_for_projects(root: Path) -> List[dict]:
    tomls = get_toml_files(root)

    return [
        {"name": get_project_name(d), "packages": get_project_package_includes(d)}
        for d in tomls
    ]


def get_project_names_and_paths(root: Path) -> List[dict]:
    project_files = get_project_files(root)

    return [
        {"name": get_project_name(get_toml(p)), "path": p.parent} for p in project_files
    ]
