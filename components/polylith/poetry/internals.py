from functools import lru_cache
from pathlib import Path
from typing import List, Union

from poetry.factory import Factory
from poetry.poetry import Poetry
from poetry.utils.env import EnvManager
from polylith import project


def get_project_poetry(path: Path) -> Poetry:
    return Factory().create_poetry(path)


@lru_cache
def distributions(path: Path) -> list:
    """Get distributions from the current Poetry project context.

    When running code within Poetry, the current environment is the one Poetry uses and
    not the environment in the current project or workspace.

    Querying importlib.metadata will fail to find the libraries added to the workspace.

    This function uses the Poetry internals to fetch the distributions,
    that internally queries the metadata based on the current path.
    """
    project_poetry = get_project_poetry(path)

    env = EnvManager(project_poetry).get()

    return list(env.site_packages.distributions())


def find_third_party_libs(path: Path) -> dict:
    project_poetry = get_project_poetry(path)

    if not project_poetry.locker.is_locked():
        raise ValueError("poetry.lock not found. Run `poetry lock` to create it.")

    packages = project_poetry.locker.locked_repository().packages

    return {p.name: str(p.version) for p in packages}


def merge_project_data(project_data: dict) -> dict:
    path = project_data["path"]

    third_party_libs = find_third_party_libs(path)
    return {
        **project_data,
        **{"deps": {"items": third_party_libs, "source": "poetry.lock"}},
    }


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
