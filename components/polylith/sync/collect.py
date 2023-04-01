from pathlib import Path
from typing import List, Set, Union

from polylith import info


def find_project_data(project_name: str, projects_data: List[dict]) -> dict:
    return next(p for p in projects_data if p["name"] == project_name)


def find_development_data(projects_data: List[dict]) -> dict:
    return next(p for p in projects_data if not info.is_project(p))


def diff(bricks: List[str], bricks_in_project: Set[str]) -> Set[str]:
    return set(bricks).difference(bricks_in_project)


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

    return {
        "bases": diff(bases, data["bases"]),
        "components": diff(components, data["components"]),
    }
