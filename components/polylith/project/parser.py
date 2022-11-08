from pathlib import Path

import tomlkit
from polylith.project.get import (
    get_project_files,
    get_project_name,
    get_project_package_includes,
    get_toml,
)


def to_path(package: dict) -> dict[str, Path | str]:
    include = package["include"]
    from_path = package.get("from")

    combined_path = Path(f"{from_path}/{include}") if from_path else Path(include)

    return {
        "path": combined_path,
        "brick": include,
    }


def to_paths(toml: tomlkit.TOMLDocument) -> list[dict[str, Path | str]]:
    packages = get_project_package_includes(toml)

    sorted_packages = sorted(packages, key=lambda p: (p["from"], p["include"]))

    return [to_path(p) for p in sorted_packages]


def to_project_package_paths(toml: tomlkit.TOMLDocument) -> dict:
    name = get_project_name(toml)
    paths = to_paths(toml)

    return {"project_name": name, "bricks": paths}


def get_projects_package_paths(path: Path) -> list[dict]:
    project_files = get_project_files(path)

    tomls = (get_toml(f) for f in project_files)

    return [to_project_package_paths(t) for t in tomls]
