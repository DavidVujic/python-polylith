from pathlib import Path
from typing import List, Set

from polylith import check, workspace


def get_brick_imports(
    root: Path, ns: str, bases: Set[str], components: Set[str]
) -> dict:
    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    comp_paths = workspace.paths.collect_components_paths(root, ns, components)

    brick_imports_in_bases = check.collect.extract_bricks(bases_paths, ns)
    brick_imports_in_components = check.collect.extract_bricks(comp_paths, ns)

    return {
        "bases": check.collect.with_unknown_components(
            root, ns, brick_imports_in_bases
        ),
        "components": check.collect.with_unknown_components(
            root, ns, brick_imports_in_components
        ),
    }


def without(key: str, bricks: Set[str]) -> Set[str]:
    return {b for b in bricks if b != key}


def sorted_usings(usings: Set[str], bases: Set[str], components: Set[str]) -> List[str]:
    usings_bases = sorted({b for b in usings if b in bases})
    usings_components = sorted({c for c in usings if c in components})

    return usings_components + usings_bases


def sorted_used_by(
    brick: str, bases: Set[str], components: Set[str], import_data: dict
) -> List[str]:
    brick_used_by = without(brick, {k for k, v in import_data.items() if brick in v})

    return sorted_usings(brick_used_by, bases, components)


def sorted_uses(
    brick: str, bases: Set[str], components: Set[str], import_data: dict
) -> List[str]:
    brick_uses = without(brick, import_data.get(brick, set()))

    return sorted_usings(brick_uses, bases, components)


def calculate_brick_deps(brick: str, bricks: dict, import_data: dict) -> dict:
    bases = bricks["bases"]
    components = bricks["components"]

    brick_used_by = sorted_used_by(brick, bases, components, import_data)
    brick_uses = sorted_uses(brick, bases, components, import_data)

    return {"used_by": brick_used_by, "uses": brick_uses}


def find_intersection_for_usings(usings: dict) -> Set[str]:
    uses = set(usings["uses"])
    used_by = set(usings["used_by"])

    return uses.intersection(used_by)


def find_bricks_with_circular_dependencies(bricks_deps: dict) -> dict:
    res = {k: find_intersection_for_usings(v) for k, v in bricks_deps.items()}

    return {k: v for k, v in sorted(res.items()) if v}
