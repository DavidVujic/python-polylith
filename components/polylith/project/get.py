from collections.abc import Generator
from pathlib import Path

import tomlkit


def get_project_name(data) -> str:
    return data.get("tool", {}).get("poetry", {}).get("name")


def get_toml(path: Path) -> dict:
    with path.open() as f:
        return tomlkit.loads(f.read())


def get_project_files(path: Path) -> Generator:
    return path.glob("projects/**/*.toml")


def get_project_names(path) -> list[str]:
    file_paths = get_project_files(path)
    tomls = (get_toml(p) for p in file_paths)

    return [get_project_name(d) for d in tomls]
