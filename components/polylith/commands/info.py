from pathlib import Path
from typing import List

from polylith import configuration, info


def filter_by(projects_data: List[dict], key: str, groups) -> List[dict]:
    return (
        [p for p in projects_data if p[key].intersection(groups)]
        if groups
        else projects_data
    )


def run(root: Path, options: dict):
    ns = configuration.get_namespace_from_config(root)
    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)
    projects_data = info.get_bricks_in_projects(root, components, bases, ns)

    groups = options.get("groups")
    teams = options.get("teams")

    filtered_by_group = filter_by(projects_data, "groups", groups)
    filtered = filter_by(filtered_by_group, "teams", teams)

    info.print_workspace_summary(projects_data, bases, components, options)

    if not components and not bases:
        return

    info.print_bricks_in_projects(filtered or projects_data, bases, components, options)
