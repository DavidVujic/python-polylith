import importlib.metadata
import re
from functools import lru_cache, reduce
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


def parsed_namespaces_from_files(dist) -> List[str]:
    name = dist.metadata["name"]
    files = dist.files or []

    normalized_name = str.replace(name, "-", "_")
    to_ignore = {
        name,
        normalized_name,
        str.lower(name),
        str.lower(normalized_name),
        "..",
    }

    filtered = [f for f in files if f.suffix == ".py"]
    top_folders = {f.parts[0] for f in filtered if len(f.parts) > 1}
    namespaces = {t for t in top_folders if t not in to_ignore}

    return list(namespaces)


def parsed_top_level_namespace(namespaces: List[str]) -> List[str]:
    return [str.replace(ns, "/", ".") for ns in namespaces]


def top_level_packages(dist) -> List[str]:
    top_level = dist.read_text("top_level.txt")

    namespaces = str.split(top_level or "")

    return parsed_top_level_namespace(namespaces) or parsed_namespaces_from_files(dist)


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


@lru_cache
def get_distributions() -> list:
    return list(importlib.metadata.distributions())


def get_packages_distributions(project_dependencies: set) -> set:
    """Return the mapped top namespace from an import

    Example:
    A third-party library, such as opentelemetry-instrumentation-fastapi.
    The return value would be the mapped top namespace: opentelemetry

    Note: available for Python >= 3.10
    """

    # added in Python 3.10
    fn = getattr(importlib.metadata, "packages_distributions", None)

    dists = fn() if fn else {}

    common = {k for k, v in dists.items() if project_dependencies.intersection(set(v))}

    return common.difference(project_dependencies)
