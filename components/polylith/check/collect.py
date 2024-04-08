from pathlib import Path
from typing import Set

from polylith import check, imports, workspace


def extract_bricks(paths: Set[Path], ns: str) -> dict:
    all_imports = imports.fetch_all_imports(paths)

    return check.grouping.extract_brick_imports(all_imports, ns)


def with_unknown_components(root: Path, ns: str, brick_imports: dict) -> dict:
    keys = set(brick_imports.keys())
    values = set().union(*brick_imports.values())

    unknowns = values.difference(keys)

    if not unknowns:
        return brick_imports

    paths = workspace.paths.collect_components_paths(root, ns, unknowns)

    extracted = extract_bricks(paths, ns)

    if not extracted:
        return brick_imports

    collected = {**brick_imports, **extracted}

    return with_unknown_components(root, ns, collected)


def diff(known_bricks: Set[str], bases: Set[str], components: Set[str]) -> Set[str]:
    bricks = set().union(bases, components)

    return known_bricks.difference(bricks)


def imports_diff(
    brick_imports: dict, bases: Set[str], components: Set[str]
) -> Set[str]:
    flattened_bases = set().union(*brick_imports["bases"].values())
    flattened_components = set().union(*brick_imports["components"].values())

    flattened_imports = set().union(flattened_bases, flattened_components)

    return diff(flattened_imports, bases, components)
