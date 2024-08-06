from pathlib import Path
from typing import List, Set, Union

from polylith import configuration, deps, diff, info, repo


def get_imports(root: Path, ns: str, bases: Set[str], components: Set[str]) -> dict:
    brick_imports = deps.get_brick_imports(root, ns, bases, components)

    return {**brick_imports["bases"], **brick_imports["components"]}


def get_projects_data(root: Path, ns: str) -> List[dict]:
    data = info.get_projects_data(root, ns)

    return [p for p in data if info.is_project(p)]


def flatten_bricks(projects_data: List[dict], brick_type: str) -> Set[str]:
    matrix = [p[brick_type] for p in projects_data]

    flattened: List[str] = sum(matrix, [])

    return set(flattened)


def flatten_dependent_bricks(
    changed_bricks: Set[str], bases: Set[str], components: Set[str], import_data: dict
) -> Set[str]:
    matrix = [
        deps.report.sorted_used_by(brick, bases, components, import_data)
        for brick in changed_bricks
    ]

    flattened: List[str] = sum(matrix, [])
    filtered = set(flattened).difference(changed_bricks)

    return filtered


def calculate_dependent_bricks(
    root: Path, ns: str, projects_data: List[dict], changed_bricks: Set[str]
) -> dict:
    bases = flatten_bricks(projects_data, "bases")
    components = flatten_bricks(projects_data, "components")
    import_data = get_imports(root, ns, bases, components)

    dependent_bricks = flatten_dependent_bricks(
        changed_bricks, bases, components, import_data
    )

    dependent_bases = {b for b in dependent_bricks if b in bases}
    dependent_components = {c for c in dependent_bricks if c in components}

    return {"bases": dependent_bases, "components": dependent_components}


def print_views(root: Path, tag: str, options: dict) -> None:
    short = options.get("short", False)
    only_bricks = options.get("bricks", False)
    with_deps = options.get("deps", False)

    ns = configuration.get_namespace_from_config(root)
    files = diff.collect.get_files(tag)

    changed_bases = diff.collect.get_changed_bases(root, files, ns)
    changed_components = diff.collect.get_changed_components(root, files, ns)
    changed_bricks = set(changed_bases + changed_components)
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

    dependent_bricks = (
        calculate_dependent_bricks(root, ns, projects_data, changed_bricks)
        if with_deps
        else {}
    )

    diff.report.print_detected_changes_in_bricks(
        changed_bases, changed_components, dependent_bricks, options
    )


def run(tag_name: Union[str, None], options: dict):
    root = repo.get_workspace_root(Path.cwd())

    tag = diff.collect.get_latest_tag(root, tag_name)

    if not tag:
        print("No tags found in repository.")
        return

    print_views(root, tag, options)
