from functools import lru_cache
from pathlib import Path

import tomlkit
from polylith.repo.repo import default_toml, is_pep_621_ready


@lru_cache
def get_pyproject_data(path: Path) -> tomlkit.TOMLDocument:
    with open(str(path / default_toml), "r", errors="ignore") as f:
        return tomlkit.loads(f.read())


def get_metadata_section(data: dict) -> dict:
    return data["project"] if is_pep_621_ready(data) else data["tool"]["poetry"]


def get_authors(path: Path) -> str:
    data = get_pyproject_data(path)
    section = get_metadata_section(data)

    authors = section.get("authors")

    return authors.as_string() if authors else ""


def get_python_version(path: Path) -> str:
    data: dict = get_pyproject_data(path)

    if is_pep_621_ready(data):
        return data["project"].get("requires-python", "")

    return data["tool"]["poetry"]["dependencies"]["python"]
