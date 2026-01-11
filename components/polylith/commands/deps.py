from pathlib import Path
from typing import List, Set

from polylith import bricks, deps, info, interface


def get_imports(root: Path, ns: str, bricks: dict) -> dict:
    bases = bricks["bases"]
    components = bricks["components"]
    brick_imports = deps.get_brick_imports(root, ns, bases, components)

    return {**brick_imports["bases"], **brick_imports["components"]}


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


def used_by_as_bricks(bricks: dict, brick_deps: dict) -> dict:
    bases = bricks["bases"]
    components = bricks["components"]

    used_by = brick_deps["used_by"]
    return {
        "bases": {b for b in used_by if b in bases},
        "components": {b for b in used_by if b in components},
    }


def run(root: Path, ns: str, options: dict):
    directory = options.get("directory")
    brick = options.get("brick")

    projects_data = info.get_projects_data(root, ns) if directory else []
    project = next((p for p in projects_data if directory in p["path"].as_posix()), {})

    bricks = {
        "bases": get_bases(root, ns, project),
        "components": get_components(root, ns, project),
    }

    imports = get_imports(root, ns, bricks)

    bricks_deps = {
        b: deps.calculate_brick_deps(b, bricks, imports)
        for b in set().union(*bricks.values())
    }

    circular_bricks = deps.find_bricks_with_circular_dependencies(bricks_deps)

    if brick and imports.get(brick):
        brick_deps = bricks_deps[brick]
        used_bricks = used_by_as_bricks(bricks, brick_deps)

        circular_deps = circular_bricks.get(brick)

        deps.print_brick_deps(brick, bricks, brick_deps, options)

        if circular_deps:
            deps.print_brick_with_circular_deps(brick, circular_deps, bricks)

        interface.report.print_brick_interface_usage(root, ns, brick, used_bricks)

        return

    deps.print_deps(bricks, imports, options)
    deps.print_bricks_with_circular_deps(circular_bricks, bricks)
