from pathlib import Path
from typing import List, Union

from polylith import configuration, deps, diff, info, repo


def get_imports(root: Path, ns: str, bases: list, components: list) -> dict:
    brick_imports = deps.get_brick_imports(root, ns, set(bases), set(components))

    return {**brick_imports["bases"], **brick_imports["components"]}


def get_projects_data(root: Path, ns: str) -> List[dict]:
    data = info.get_projects_data(root, ns)

    return [p for p in data if info.is_project(p)]


def print_views(root: Path, tag: str, options: dict) -> None:
    short = options.get("short", False)
    only_bricks = options.get("bricks", False)
    with_deps = only_bricks and options.get("deps", False)

    ns = configuration.get_namespace_from_config(root)
    files = diff.collect.get_files(tag)

    changed_bases = diff.collect.get_changed_bases(root, files, ns)
    changed_components = diff.collect.get_changed_components(root, files, ns)
    changed_projects = diff.collect.get_changed_projects(files)

    projects_data = get_projects_data(root, ns)

    if not short and not only_bricks:
        diff.report.print_diff_summary(tag, changed_bases, changed_components)
        diff.report.print_detected_changes_in_projects(changed_projects, short)
        diff.report.print_diff_details(projects_data, changed_bases, changed_components)

        return

    if short and not only_bricks:
        affected_projects = diff.collect.get_projects_affected_by_changes(
            projects_data, changed_projects, changed_bases, changed_components
        )
        diff.report.print_projects_affected_by_changes(affected_projects, short)

        return

    imports = (
        get_imports(root, ns, changed_bases, changed_components) if with_deps else {}
    )

    diff.report.print_detected_changes_in_bricks(
        changed_bases, changed_components, imports, options
    )


def run(tag_name: Union[str, None], options: dict):
    root = repo.get_workspace_root(Path.cwd())

    tag = diff.collect.get_latest_tag(root, tag_name)

    if not tag:
        print("No tags found in repository.")
        return

    print_views(root, tag, options)
