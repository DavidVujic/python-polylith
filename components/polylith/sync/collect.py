from pathlib import Path
from typing import List, Set

from polylith import check, imports, info, workspace


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


def get_brick_imports(root: Path, ns: str, project_data: dict) -> dict:
    bases = {b for b in project_data.get("bases", [])}
    components = {c for c in project_data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    brick_imports_in_bases = extract_bricks(bases_paths, ns)
    brick_imports_in_components = extract_bricks(components_paths, ns)

    return {
        "bases": with_unknown_components(root, ns, brick_imports_in_bases),
        "components": with_unknown_components(root, ns, brick_imports_in_components),
    }


def diff(known_bricks: Set[str], bases: List[str], components: List[str]) -> Set[str]:
    bricks = set().union(bases, components)

    return known_bricks.difference(bricks)


def imports_diff(brick_imports: dict, bases: List, components: List) -> Set[str]:
    flattened_bases = set().union(*brick_imports["bases"].values())
    flattened_components = set().union(*brick_imports["components"].values())

    flattened_imports = set().union(flattened_bases, flattened_components)

    return diff(flattened_imports, bases, components)


def calculate_diff(
    root: Path,
    namespace: str,
    project_data: dict,
    workspace_data: dict,
) -> dict:
    brick_imports = get_brick_imports(root, namespace, project_data)

    all_bases = workspace_data["bases"]
    all_components = workspace_data["components"]

    bases = project_data["bases"]
    components = project_data["components"]

    is_project = info.is_project(project_data)

    if is_project:
        brick_diff = imports_diff(brick_imports, bases, components)
    else:
        all_bricks = set().union(all_bases, all_components)
        brick_diff = diff(all_bricks, bases, components)

    bases_diff = {b for b in brick_diff if b in all_bases}
    components_diff = {b for b in brick_diff if b in all_components}

    return {
        "name": project_data["name"],
        "path": project_data["path"],
        "is_project": is_project,
        "bases": bases_diff,
        "components": components_diff,
    }
