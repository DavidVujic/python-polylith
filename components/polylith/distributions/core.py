import importlib.metadata
import re
from functools import reduce
from typing import Dict, List, Set


SUB_DEP_SEPARATORS = r"[\s!=;><\^~]"


def top_level_packages(dist) -> List[str]:
    top_level = dist.read_text("top_level.txt")

    return str.split(top_level or "")


def mapped_packages(dist) -> dict:
    packages = top_level_packages(dist)
    name = dist.metadata["name"]

    return {name: packages} if packages else {}


def map_packages(acc, dist) -> dict:
    return {**acc, **mapped_packages(dist)}


def only_package_name(package: str) -> str:
    parts = re.split(SUB_DEP_SEPARATORS, package)

    return str(parts[0])


def dist_subpackages(dist) -> Set[str]:
    packages = importlib.metadata.requires(dist.metadata["name"]) or []

    return {only_package_name(p) for p in packages}


def distributions_subpackages(dists) -> Set[str]:
    res = [dist_subpackages(dist) for dist in dists]

    return set().union(*res)


def distributions_packages(dists) -> Dict[str, List[str]]:
    """Return a mapping of top-level packages to their distributions.

    Additional dist sub-dependency package names (without dist names) are appended to the result.
    """
    mapped: dict = reduce(map_packages, dists, {})

    sub_packages = distributions_subpackages(dists)
    reshaped = {s: [s] for s in sub_packages}

    return {**reshaped, **mapped}


def get_distributions(project_dependencies: set) -> list:
    dists = importlib.metadata.distributions()

    return [dist for dist in dists if dist.metadata["name"] in project_dependencies]
