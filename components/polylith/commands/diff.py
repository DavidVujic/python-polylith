from pathlib import Path

from typing import Union
from polylith import diff, info, repo, workspace


def print_views(root: Path, tag: str, short: bool, only_bricks: bool) -> None:
    ns = workspace.parser.get_namespace_from_config(root)
    files = diff.collect.get_files(tag)
    bases = diff.collect.get_changed_bases(files, ns)
    components = diff.collect.get_changed_components(files, ns)

    projects = diff.collect.get_changed_projects(files)
    all_projects_data = info.get_bricks_in_projects(root, components, bases, ns)
    projects_data = [p for p in all_projects_data if info.is_project(p)]

    affected_projects = diff.collect.get_projects_affected_by_changes(
        projects_data, projects, bases, components
    )

    if not short and not only_bricks:
        diff.report.print_diff_summary(tag, bases, components)
        diff.report.print_detected_changes_in_projects(projects, short)
        diff.report.print_diff_details(projects_data, bases, components)

        return

    if short and not only_bricks:
        diff.report.print_projects_affected_by_changes(affected_projects, short)

        return

    diff.report.print_detected_changes_in_bricks(bases, components, short)


def run(tag_name: Union[str, None], short: bool, only_bricks: bool):
    root = repo.get_workspace_root(Path.cwd())

    tag = diff.collect.get_latest_tag(root, tag_name)

    if not tag:
        print("No tags found in repository.")
        return

    print_views(root, tag, short, only_bricks)
