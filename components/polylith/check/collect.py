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


def flatten_imported_bricks(imports: dict) -> Set[str]:
    return set().union(*imports.values())


def to_flattened_imports(brick_imports: dict) -> Set[str]:
    flattened_bases = flatten_imported_bricks(brick_imports["bases"])
    flattened_components = flatten_imported_bricks(brick_imports["components"])

    return set().union(flattened_bases, flattened_components)


def imports_diff(
    brick_imports: dict, bases: Set[str], components: Set[str]
) -> Set[str]:
    flattened_imports = to_flattened_imports(brick_imports)

    return diff(flattened_imports, bases, components)


def is_used(brick: str, imported_bricks: dict) -> bool:
    return any(k for k, v in imported_bricks.items() if k != brick and brick in v)


def find_unused_bricks(
    brick_imports: dict, bases: Set[str], components: Set[str]
) -> Set[str]:
    all_brick_imports = {**brick_imports["bases"], **brick_imports["components"]}

    bricks = to_flattened_imports(brick_imports).difference(bases)
    used_bricks = {brick for brick in bricks if is_used(brick, all_brick_imports)}

    return components.difference(used_bricks)
