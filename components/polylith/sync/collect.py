from pathlib import Path
from typing import List, Set

from polylith import check, imports, info, workspace


def get_brick_imports(root: Path, ns: str, project_data: dict) -> dict:
    bases = {b for b in project_data.get("bases", [])}
    components = {c for c in project_data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    all_imports_in_bases = imports.fetch_all_imports(bases_paths)
    all_imports_in_components = imports.fetch_all_imports(components_paths)

    return {
        "bases": check.grouping.extract_brick_imports(all_imports_in_bases, ns),
        "components": check.grouping.extract_brick_imports(
            all_imports_in_components, ns
        ),
    }


def diff(known_bricks: Set[str], bases: List[str], components: List[str]) -> Set[str]:
    bricks = set().union(bases, components)

    return known_bricks.difference(bricks)


def imports_diff(imports: dict, bases: List, components: List) -> Set[str]:
    flattened_bases = set().union(*imports["bases"].values())
    flattened_components = set().union(*imports["components"].values())

    flattened_imports = set().union(flattened_bases, flattened_components)

    return diff(flattened_imports, bases, components)


def calculate_diff(
    root: Path,
    namespace: str,
    project_data: dict,
    workspace_data: dict,
) -> dict:
    imports = get_brick_imports(root, namespace, project_data)

    all_bases = workspace_data["bases"]
    all_components = workspace_data["components"]

    bases = project_data["bases"]
    components = project_data["components"]

    is_project = info.is_project(project_data)

    if is_project:
        brick_diff = imports_diff(imports, bases, components)
    else:
        all_bricks = set().union(all_bases, all_components)
        brick_diff = diff(all_bricks, bases, components)

    return {
        "name": project_data["name"],
        "path": project_data["path"],
        "is_project": is_project,
        "bases": {b for b in brick_diff if b in all_bases},
        "components": {b for b in brick_diff if b in all_components},
    }
