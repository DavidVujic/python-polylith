from pathlib import Path
from typing import List, Set, Union

from polylith import check, imports, info, workspace


def find_project_data(project_name: str, projects_data: List[dict]) -> dict:
    return next(p for p in projects_data if p["name"] == project_name)


def find_development_data(projects_data: List[dict]) -> dict:
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


def diff(imported_bricks: dict, project_data: dict) -> Set[str]:
    flattened = set().union(*imported_bricks.values())

    b = set(project_data["bases"])
    c = set(project_data["components"])

    project_bricks = set().union(b, c)

    return flattened.difference(project_bricks)


def calculate_difference(
    root: Path, namespace: str, project_name: Union[str, None]
) -> dict:
    bases = info.get_bases(root, namespace)
    components = info.get_components(root, namespace)
    projects_data = info.get_bricks_in_projects(root, components, bases, namespace)

    if project_name:
        data = find_project_data(project_name, projects_data)
    else:
        data = find_development_data(projects_data)

    brick_imports = get_brick_imports(root, namespace, data)

    bases_diff = diff(brick_imports["bases"], data)
    components_diff = diff(brick_imports["components"], data)

    return {
        "bases": bases_diff,
        "components": components_diff,
    }
