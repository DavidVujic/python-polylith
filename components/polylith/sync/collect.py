from pathlib import Path

from polylith import info, workspace


def get_missing_bricks(root: Path):
    ns = workspace.parser.get_namespace_from_config(root)
    projects_data = info.get_projects_data(root, ns)

    return projects_data
