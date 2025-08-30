from pathlib import Path

from polylith import configuration, info


def run(root: Path, options: dict):
    ns = configuration.get_namespace_from_config(root)
    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)
    projects_data = info.get_bricks_in_projects(root, components, bases, ns)

    info.print_workspace_summary(projects_data, bases, components, options)

    if not components and not bases:
        return

    info.print_bricks_in_projects(projects_data, bases, components, options)
