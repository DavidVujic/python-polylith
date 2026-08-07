from pathlib import Path
from typing import List, Set, Tuple, Union

from polylith import configuration, diff, dirs, info, test


def get_imported_bricks_in_tests(
    root: Path, ns: str, tag_name: Union[str, None], theme: str
) -> Set[str]:
    files = test.get_changed_files(root, tag_name)
    brick_imports = test.get_brick_imports_in_tests(root, ns, theme, files)

    return set().union(*brick_imports.values())


def extract_brick_names(bricks_data: List[dict], possible_bricks: Set[str]) -> Set[str]:
    return {v for b in bricks_data for v in b.values() if v in possible_bricks}


def get_affected_bricks(
    root: Path, ns: str, tag_name: Union[str, None], theme: str
) -> Tuple[Set[str], Set[str]]:
    found = get_imported_bricks_in_tests(root, ns, tag_name, theme)

    bases = extract_brick_names(dirs.get_bases_data(root, ns), found)
    components = extract_brick_names(dirs.get_components_data(root, ns), found)

    return bases, components


def get_related_bricks(
    root: Path, ns: str, tag_name: Union[str, None], theme: str
) -> Tuple[Set[str], Set[str]]:
    files = test.get_changed_files(root, tag_name)
    related = test.get_related_bricks(root, ns, theme, files)

    bases = extract_brick_names(dirs.get_bases_data(root, ns), related["bases"])
    components = extract_brick_names(dirs.get_components_data(root, ns), related["components"])

    return bases, components


def get_affected_projects(
    root: Path, ns: str, bases: Set[str], components: Set[str]
) -> List[dict]:
    projects_data = [p for p in info.get_projects_data(root, ns) if info.is_project(p)]

    names = diff.collect.get_projects_affected_by_changes(
        projects_data, [], list(bases), list(components)
    )

    return [p for p in projects_data if p["path"].name in names]


def parse_strategy(strategy: str) -> List[str]:
    strategies = str.split(strategy, ",")

    return [str.lower(s) for s in strategies]


def run(root: Path, ns: str, tag: str, options: dict) -> None:
    theme = configuration.get_theme_from_config(root)

    strategy = parse_strategy(options["strategy"])

    by_imports = "imports" in strategy
    by_path = "path" in strategy

    fallback: Tuple[Set[str], Set[str]] = set(), set()
    affected = get_affected_bricks(root, ns, tag, theme) if by_imports else fallback
    related = get_related_bricks(root, ns, tag, theme) if by_path else fallback

    bases = set().union(affected[0], related[0])
    components = set().union(affected[1], related[1])

    projects_data = get_affected_projects(root, ns, bases, components)

    if options.get("bricks"):
        test.report.print_detected_changes_affecting_bricks(bases, components, options)
        return

    if options.get("projects"):
        test.report.print_projects_affected_by_changes(projects_data, options)
        return

    test.report.print_report_summary(projects_data, bases, components, tag)
    test.report.print_test_report(projects_data, bases, components, options)
