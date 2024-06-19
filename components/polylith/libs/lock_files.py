from pathlib import Path
from typing import Set

import tomlkit


def find_lock_file(project_data: dict) -> dict:
    directory = project_data["path"]

    variants = {
        "pdm.lock": "toml",
        "requirements.lock": "text",
        "requirements.txt": "text",
    }

    return {k: v for k, v in variants.items() if Path(directory / k).exists()}


def extract_lib_names_from_toml(path: Path, filename: str) -> Set[str]:
    with open(path / filename, "r") as f:
        try:
            data = tomlkit.load(f)
        except tomlkit.exceptions.ParseError:
            return set()

    return {p.get("name") for p in data.get("package", [])}


def extract_lib_names_from_txt(path: Path, filename: str) -> Set[str]:
    with open(path / filename, "r") as f:
        data = f.readlines()

    rows = (str.strip(line) for line in data)
    filtered = (row for row in rows if row and not row.startswith(("#", "-")))
    parts = (str.split(row, "==") for row in filtered)

    return {row[0] for row in parts}


def extract_lib_names(project_data: dict, lock_file_data: dict) -> Set[str]:
    first = next(iter(lock_file_data.items()), None)

    if not first:
        return set()

    path = project_data["path"]
    filename, filetype = first

    if filetype == "toml":
        return extract_lib_names_from_toml(path, filename)

    return extract_lib_names_from_txt(path, filename)
