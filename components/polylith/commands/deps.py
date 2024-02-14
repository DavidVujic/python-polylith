from pathlib import Path
from typing import List, Set, Union

from polylith import bricks, deps, info


def print_report(root: Path, ns: str, bases: Set[str], components: Set[str]):
    brick_imports = deps.get_brick_imports(root, ns, bases, components)

    flattened = {**brick_imports["bases"], **brick_imports["components"]}

    deps.print_deps(bases, components, flattened)


def pick_name(data: List[dict]) -> Set[str]:
    return {b["name"] for b in data}


def get_bases(root: Path, ns: str, project_data: dict) -> Set[str]:
    if project_data:
        return set(project_data.get("bases", []))

    return pick_name(bricks.get_bases_data(root, ns))


def get_components(root: Path, ns: str, project_data: dict) -> Set[str]:
    if project_data:
        return set(project_data.get("components", []))

    return pick_name(bricks.get_components_data(root, ns))


def run(root: Path, ns: str, directory: Union[str, None]):
    projects_data = info.get_projects_data(root, ns) if directory else []
    project = next((p for p in projects_data if directory in p["path"].as_posix()), {})

    bases = get_bases(root, ns, project)
    components = get_components(root, ns, project)

    print_report(root, ns, bases, components)
