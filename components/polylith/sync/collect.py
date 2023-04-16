from pathlib import Path
from typing import List, Set, Union

from polylith import check, imports, info, workspace


def find_project_data(
    projects_data: List[dict], project_name: Union[str, None]
) -> dict:
    if project_name:
        return next(p for p in projects_data if p["name"] == project_name)

    return next(p for p in projects_data if not info.is_project(p))


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


def diff(brick_imports: dict, project_data: dict) -> Set[str]:
    flattened_bases = set().union(*brick_imports["bases"].values())
    flattened_components = set().union(*brick_imports["components"].values())

    flattened = set().union(flattened_bases, flattened_components)

    b = set(project_data["bases"])
    c = set(project_data["components"])

    project_bricks = set().union(b, c)

    return flattened.difference(project_bricks)


def calculate_difference(
    root: Path,
    namespace: str,
    project_name: Union[str, None],
) -> dict:
    all_bases = info.get_bases(root, namespace)
    all_components = info.get_components(root, namespace)
    all_projects_data = info.get_bricks_in_projects(
        root, all_components, all_bases, namespace
    )

    project_data = find_project_data(all_projects_data, project_name)

    brick_imports = get_brick_imports(root, namespace, project_data)
    brick_diff = diff(brick_imports, project_data)

    return {
        "bases": {b for b in brick_diff if b in all_bases},
        "components": {b for b in brick_diff if b in all_components},
    }
