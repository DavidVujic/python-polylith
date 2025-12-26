from functools import partial
from pathlib import Path
from typing import Set

from polylith import check, configuration, deps, info


def _is_empty(brick: str, bricks_path: Path) -> bool:
    path = bricks_path / brick

    return not any(path.iterdir())


def _without_empty(
    root: Path, namespace: str, bricks: Set[str], brick_type: str
) -> Set[str]:
    theme = configuration.get_theme_from_config(root)

    if theme == "loose":
        bricks_path = root / f"{brick_type}/{namespace}"
    else:
        bricks_path = root / f"{brick_type}"

    return {brick for brick in bricks if not _is_empty(brick, bricks_path)}


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
    comp_diff = {b for b in brick_diff if b in all_components}

    fn = partial(_without_empty, root, namespace)

    return {
        "name": project_data["name"],
        "path": project_data["path"],
        "is_project": is_project,
        "bases": bases_diff if is_project else fn(bases_diff, "bases"),
        "components": comp_diff if is_project else fn(comp_diff, "components"),
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
