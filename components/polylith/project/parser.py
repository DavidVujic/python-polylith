from pathlib import Path

import tomlkit
from polylith.project.get import (
    get_project_files,
    get_project_name,
    get_project_package_includes,
    get_toml,
)


def to_path(package: dict) -> Path:
    include = package["include"]
    from_path = package.get("from")

    return Path(f"{from_path}/{include}") if from_path else Path(include)


def to_paths(toml: tomlkit.TOMLDocument) -> list[Path]:
    packages = get_project_package_includes(toml)

    return [to_path(p) for p in packages]


def to_project_package_paths(toml: tomlkit.TOMLDocument) -> dict:
    name = get_project_name(toml)
    paths = to_paths(toml)

    return {"name": name, "paths": paths}


def get_projects_package_paths(path: Path) -> list[dict]:
    project_files = get_project_files(path)

    tomls = (get_toml(f) for f in project_files)

    return [to_project_package_paths(t) for t in tomls]
