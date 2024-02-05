from pathlib import Path

from polylith import configuration, info, repo


def run(short: bool):
    root = repo.get_workspace_root(Path.cwd())

    ns = configuration.get_namespace_from_config(root)
    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)
    projects_data = info.get_bricks_in_projects(root, components, bases, ns)

    info.print_workspace_summary(projects_data, bases, components)

    if not components and not bases:
        return

    if short:
        info.print_compressed_view_for_bricks_in_projects(
            projects_data, bases, components
        )
    else:
        info.print_bricks_in_projects(projects_data, bases, components)
