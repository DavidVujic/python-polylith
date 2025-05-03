from pathlib import Path
from typing import List, Set, Union

from polylith import bricks, configuration, diff, info, repo, test


def get_imported_bricks_in_tests(
    root: Path, ns: str, tag_name: Union[str, None], theme: str
) -> Set[str]:
    files = test.get_changed_files(root, tag_name)
    brick_imports = test.get_brick_imports_in_tests(root, ns, theme, files)

    return set().union(*brick_imports.values())


def extract_bricks(bricks_data: List[dict], imported_bricks: Set[str]) -> Set[str]:
    return {v for b in bricks_data for v in b.values() if v in imported_bricks}


def get_imported_bricks(
    root: Path, ns: str, tag_name: Union[str, None], theme: str
) -> dict:
    found = get_imported_bricks_in_tests(root, ns, tag_name, theme)

    bases = extract_bricks(bricks.get_bases_data(root, ns), found)
    components = extract_bricks(bricks.get_components_data(root, ns), found)

    return {"bases": bases, "components": components}


def run(tag_name: Union[str, None], options: dict):
    root = repo.get_workspace_root(Path.cwd())

    tag = diff.collect.get_latest_tag(root, tag_name) or tag_name

    if not tag:
        print("No matching tags or commits found in repository.")
        return

    ns = configuration.get_namespace_from_config(root)
    theme = configuration.get_theme_from_config(root)

    imported_bricks = get_imported_bricks(root, ns, tag_name, theme)
    bases = imported_bricks["bases"]
    components = imported_bricks["components"]

    projects_data = [p for p in info.get_projects_data(root, ns) if info.is_project(p)]

    affected_projects = diff.collect.get_projects_affected_by_changes(projects_data, [], bases, components)

    test.report.print_projects_affected_by_changes(affected_projects, False)
    test.report.print_diff_summary(tag, bases, components)
    test.report.print_detected_changes_affecting_bricks(bases, components, options)
