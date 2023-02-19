from pathlib import Path
from typing import List, Set

from polylith import repo
from polylith.workspace import parser


def get_path(structure: str, brick: str, ns: str, package: str) -> str:
    return structure.format(brick=brick, namespace=ns, package=package)


def get_paths(structure: str, brick: str, ns: str, packages: List[str]) -> Set[str]:
    return {get_path(structure, brick, ns, p) for p in packages}


def collect_brick_paths(
    root: Path, ns: str, bases: List[str], components: List[str]
) -> Set[Path]:
    structure = parser.get_brick_structure_from_config(root)

    a = get_paths(structure, repo.bases_dir, ns, bases)
    b = get_paths(structure, repo.components_dir, ns, components)

    brick_paths = set().union(a, b)

    return {Path(root / p) for p in brick_paths}
