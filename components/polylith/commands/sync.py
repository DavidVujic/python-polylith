from pathlib import Path
from typing import Union

from polylith import info, project, sync


def is_project_without_bricks(project_data: dict) -> bool:
    bases = project_data["bases"]
    components = project_data["components"]

    return not bases and not components


def choose_base(root: Path, ns: str, project_data: dict) -> Union[str, None]:
    possible_bases = info.find_unused_bases(root, ns)

    if not possible_bases:
        return None

    return project.interactive.choose_base_for_project(
        root, ns, project_data["name"], possible_bases
    )


def calculate_brick_diff(root: Path, ns: str, project_data: dict) -> dict:
    if info.is_project(project_data) and is_project_without_bricks(project_data):
        base = choose_base(root, ns, project_data)

        if base:
            return sync.calculate_needed_bricks(root, ns, project_data, base)

    return sync.calculate_diff(root, ns, project_data)


def run(root: Path, ns: str, project_data: dict, options: dict):
    is_quiet = options["quiet"]
    is_verbose = options["verbose"]

    diff = calculate_brick_diff(root, ns, project_data)

    sync.update_project(root, ns, diff)

    if is_quiet:
        return

    sync.report.print_summary(diff)

    if is_verbose:
        sync.report.print_brick_imports(diff)
