from pathlib import Path
from typing import List

from polylith.bricks import base, component
from polylith.project import get_packages_for_projects, parse_package_paths


def get_matching_bricks(
    paths: List[Path], bricks: List[str], namespace: str
) -> List[str]:
    paths_in_namespace = (p.name for p in paths if p.parent.name == namespace)

    res = set(bricks).intersection(paths_in_namespace)

    return sorted(list(res))


def get_project_bricks(project_packages: List[dict], components, bases, namespace: str):
    paths = parse_package_paths(project_packages)

    components_in_project = get_matching_bricks(paths, components, namespace)
    bases_in_project = get_matching_bricks(paths, bases, namespace)

    return {"components": components_in_project, "bases": bases_in_project}


def get_components(root: Path, namespace: str) -> List[str]:
    return [c["name"] for c in component.get_components_data(root, namespace)]


def get_bases(root: Path, namespace: str) -> List[str]:
    return [b["name"] for b in base.get_bases_data(root, namespace)]


def get_bricks_in_projects(
    root: Path, components: List[str], bases: List[str], namespace: str
) -> List[dict]:
    packages_for_projects = get_packages_for_projects(root)

    res = [
        {
            **{"name": p["name"], "path": p["path"], "type": p["type"]},
            **get_project_bricks(p["packages"], components, bases, namespace),
        }
        for p in packages_for_projects
    ]

    return res


def get_projects_data(root: Path, ns: str) -> List[dict]:
    bases = get_bases(root, ns)
    components = get_components(root, ns)

    return get_bricks_in_projects(root, components, bases, ns)
