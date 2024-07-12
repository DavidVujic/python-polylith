from functools import lru_cache
from pathlib import Path
from typing import List, Union

from poetry.factory import Factory
from poetry.poetry import Poetry
from poetry.utils.env import EnvManager
from polylith import project


def get_project_poetry(poetry: Poetry, path: Union[Path, None]) -> Poetry:
    return Factory().create_poetry(path) if path else poetry


@lru_cache
def distributions(poetry: Poetry, path: Union[Path, None]) -> list:
    project_poetry = get_project_poetry(poetry, path)

    env = EnvManager(project_poetry).get()

    return list(env.site_packages.distributions())


def find_third_party_libs(poetry: Poetry, path: Union[Path, None]) -> dict:
    project_poetry = get_project_poetry(poetry, path)

    if not project_poetry.locker.is_locked():
        raise ValueError("poetry.lock not found. Run `poetry lock` to create it.")

    packages = project_poetry.locker.locked_repository().packages

    return {p.name: str(p.version) for p in packages}


def filter_projects_data(
    poetry: Poetry, directory: Union[str, None], projects_data: List[dict]
) -> List[dict]:
    if not directory:
        return projects_data

    project_name = project.get_project_name(poetry.pyproject.data)

    data = next((p for p in projects_data if p["name"] == project_name), None)

    if not data:
        raise ValueError(f"Didn't find project in {directory}")

    return [data]
