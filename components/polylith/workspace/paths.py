from pathlib import Path
from typing import Set

from polylith import repo
from polylith.workspace import parser


def get_path(structure: str, brick: str, ns: str, package: str) -> str:
    return structure.format(brick=brick, namespace=ns, package=package)


def get_paths(structure: str, brick: str, ns: str, packages: Set[str]) -> Set[str]:
    return {get_path(structure, brick, ns, p) for p in packages}


def collect_paths(root: Path, ns: str, brick: str, packages: Set[str]) -> Set[Path]:
    structure = parser.get_brick_structure_from_config(root)

    paths = get_paths(structure, brick, ns, packages)

    return {Path(root / p) for p in paths}


def collect_bases_paths(root: Path, ns: str, bases: Set[str]) -> Set[Path]:
    return collect_paths(root, ns, repo.bases_dir, bases)


def collect_components_paths(root: Path, ns: str, components: Set[str]) -> Set[Path]:
    return collect_paths(root, ns, repo.components_dir, components)
