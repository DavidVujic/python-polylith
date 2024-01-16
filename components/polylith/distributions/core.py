import importlib.metadata
import re
from functools import reduce
from typing import Dict, List


SUB_DEP_SEPARATORS = r"[\s!=;><\^~]"


def parse_sub_package_name(dependency: str) -> str:
    parts = re.split(SUB_DEP_SEPARATORS, dependency)

    return str(parts[0])


def dist_subpackages(dist) -> dict:
    name = dist.metadata["name"]
    dependencies = importlib.metadata.requires(name) or []

    parsed_package_names = list({parse_sub_package_name(d) for d in dependencies})

    return {name: parsed_package_names} if dependencies else {}


def map_sub_packages(acc, dist) -> dict:
    return {**acc, **dist_subpackages(dist)}


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


def distributions_sub_packages(dists) -> Dict[str, List[str]]:
    """Return the dependencies of each distribution."""
    return reduce(map_sub_packages, dists, {})


def get_distributions(project_dependencies: set) -> list:
    dists = importlib.metadata.distributions()

    return [dist for dist in dists if dist.metadata["name"] in project_dependencies]
