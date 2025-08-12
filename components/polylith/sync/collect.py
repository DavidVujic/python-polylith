from pathlib import Path
from typing import Set

from polylith import check, deps, info


def _calculate(root: Path, namespace: str, project_data: dict, bases: Set[str]) -> dict:
    components = set(project_data["components"])

    all_bases = info.get_bases(root, namespace)
    all_components = info.get_components(root, namespace)

    brick_imports = deps.get_brick_imports(root, namespace, bases, components)
    is_project = info.is_project(project_data)

    if is_project:
        brick_diff = check.collect.imports_diff(brick_imports, bases, components)
    else:
        all_bricks = set().union(all_bases, all_components)
        brick_diff = check.collect.diff(all_bricks, bases, components)

    bases_diff = {b for b in brick_diff if b in all_bases}
    components_diff = {b for b in brick_diff if b in all_components}

    return {
        "name": project_data["name"],
        "path": project_data["path"],
        "is_project": is_project,
        "bases": bases_diff,
        "components": components_diff,
        "brick_imports": brick_imports,
    }


def calculate_diff(root: Path, namespace: str, project_data: dict) -> dict:
    bases = set(project_data["bases"])

    return _calculate(root, namespace, project_data, bases)


def calculate_needed_bricks(
    root: Path, namespace: str, project_data: dict, base: str
) -> dict:
    bases = {base}

    res = _calculate(root, namespace, project_data, bases)

    needed_bases = res["bases"].union(bases)

    return {**res, **{"bases": needed_bases}}
