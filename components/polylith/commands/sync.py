from pathlib import Path

from polylith import info
from polylith import sync


def run(root: Path, ns: str, project_data: dict, options: dict):
    is_quiet = options["quiet"]
    is_verbose = options["verbose"]

    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)
    workspace_data = {"bases": bases, "components": components}

    diff = sync.calculate_diff(root, ns, project_data, workspace_data)

    sync.update_project(root, ns, diff)

    if is_quiet:
        return

    sync.report.print_summary(diff)

    if is_verbose:
        sync.report.print_brick_imports(diff)
