import importlib.metadata
from functools import reduce
from typing import Dict, List


def top_level_packages(dist) -> List[str]:
    top_level = dist.read_text("top_level.txt")

    return str.split(top_level or "")


def mapped_packages(dist) -> dict:
    packages = top_level_packages(dist)
    name = dist.metadata["name"]

    return {name: packages} if packages else {}


def map_packages(acc, dist) -> dict:
    return {**acc, **mapped_packages(dist)}


def distributions_packages(dists) -> Dict[str, List[str]]:
    """Return a mapping of top-level packages to their distributions."""
    return reduce(map_packages, dists, {})


def get_distributions(project_dependencies: set) -> list:
    dists = importlib.metadata.distributions()

    return [dist for dist in dists if dist.metadata["name"] in project_dependencies]
