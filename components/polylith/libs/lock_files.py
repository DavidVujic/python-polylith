from pathlib import Path
from typing import Set

import tomlkit


def find_lock_files(project_data: dict) -> dict:
    directory = project_data["path"]

    variants = {
        "pdm.lock": "toml",
        "requirements.lock": "text",
        "requirements.txt": "text",
    }

    return {k: v for k, v in variants.items() if Path(directory / k).exists()}


def pick_lock_file(project_data: dict) -> dict:
    data = find_lock_files(project_data)
    first = next(iter(data.items()), None)

    if not first:
        return {}

    filename, filetype = first

    return {"filename": filename, "filetype": filetype}


def extract_lib_names_from_toml(path: Path) -> Set[str]:
    with open(path, "r") as f:
        try:
            data = tomlkit.load(f)
        except tomlkit.exceptions.ParseError:
            return set()

    return {p.get("name") for p in data.get("package", [])}


def extract_lib_names_from_txt(path: Path) -> Set[str]:
    with open(path, "r") as f:
        data = f.readlines()

    rows = (str.strip(line) for line in data)
    filtered = (row for row in rows if row and not row.startswith(("#", "-")))
    parts = (str.split(row, "==") for row in filtered)

    return {row[0] for row in parts}


def extract_lib_names(project_data: dict, filename: str, filetype: str) -> Set[str]:
    dir_path = project_data["path"]

    path = Path(dir_path / filename)

    if not path.exists():
        return set()

    if filetype == "toml":
        return extract_lib_names_from_toml(path)

    return extract_lib_names_from_txt(path)


def extract_libs_from_lock_file(project_data: dict) -> Set[str]:
    lock_file_data = pick_lock_file(project_data)

    return extract_lib_names(project_data, **lock_file_data)
