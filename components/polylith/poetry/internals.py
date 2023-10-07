from collections import defaultdict
from functools import reduce
from pathlib import Path
from typing import DefaultDict, Dict, List, Set, Union

from poetry.factory import Factory
from poetry.poetry import Poetry
from poetry.utils.env import EnvManager


def top_level_packages(dist) -> List[str]:
    top_level = dist.read_text("top_level.txt")

    return str.split(top_level or "")


def mapped_packages(dist) -> dict:
    packages = top_level_packages(dist)
    name = dist.metadata["name"]

    return {name: package for package in packages}


def map_packages(acc, dist) -> dict:
    return {**acc, **mapped_packages(dist)}


def distributions_packages(dists) -> Dict[str, List[str]]:
    """Return a mapping of top-level packages to their distributions."""
    return reduce(map_packages, dists, {})


def distributions(poetry: Poetry, path: Union[Path, None]):
    project_poetry = Factory().create_poetry(path) if path else poetry
    env = EnvManager(project_poetry).get()

    return env.site_packages.distributions()


def packages_distributions(
    poetry: Poetry, path: Union[Path, None]
) -> DefaultDict[str, List[str]]:
    project_poetry = Factory().create_poetry(path) if path else poetry

    env = EnvManager(project_poetry).get()
    pkg_to_dist = defaultdict(list)
    for dist in env.site_packages.distributions():
        for pkg in (dist.read_text("top_level.txt") or "").split():
            pkg_to_dist[dist.metadata["Name"]].append(pkg)

    return pkg_to_dist


def find_third_party_libs(poetry: Poetry, path: Union[Path, None]) -> Set:
    project_poetry = Factory().create_poetry(path) if path else poetry

    if not project_poetry.locker.is_locked():
        raise ValueError("poetry.lock not found. Run `poetry lock` to create it.")

    packages = project_poetry.locker.locked_repository().packages

    return {p.name for p in packages}
