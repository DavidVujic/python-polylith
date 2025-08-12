from pathlib import Path

from polylith import sync


def run(root: Path, ns: str, project_data: dict, options: dict):
    is_quiet = options["quiet"]
    is_verbose = options["verbose"]

    diff = sync.calculate_diff(root, ns, project_data)

    sync.update_project(root, ns, diff)

    if is_quiet:
        return

    sync.report.print_summary(diff)

    if is_verbose:
        sync.report.print_brick_imports(diff)
