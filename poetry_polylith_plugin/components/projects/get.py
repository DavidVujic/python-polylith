from pathlib import Path

import tomlkit


def get_project_name(data):
    return data.get("tool", {}).get("poetry", {}).get("name")


def get_toml(path: Path) -> dict:
    with path.open() as f:
        return tomlkit.loads(f.read())


def get_project_files(path: Path):
    return path.glob("projects/**/*.toml")


def get_project_names(path):
    file_paths = get_project_files(path) or []
    tomls = (get_toml(p) for p in file_paths)

    return [get_project_name(d) for d in tomls]
