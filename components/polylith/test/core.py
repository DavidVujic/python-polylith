from functools import reduce
from pathlib import Path
from typing import List, Set

from polylith import check, diff, info, workspace


def get_brick_imports(root: Path, ns: str, paths: Set[Path]) -> dict:
    folders = {p if p.is_dir() else p.parent for p in paths}

    brick_imports_in_tests = check.collect.extract_bricks(folders, ns)

    return check.collect.with_unknown_components(root, ns, brick_imports_in_tests)


def get_projects_affected_by_changes(
    projects_data: List[dict], brick_imports: dict
) -> Set[str]:
    names = set().union(*brick_imports.values())
    bricks = list(names)

    return diff.collect.get_projects_affected_by_changes(
        projects_data, [], bricks, bricks
    )


def append_bricks(acc: Set[str], brick_type: str, project_data: dict) -> Set[str]:
    bricks = project_data.get(brick_type, [])

    return acc.union(bricks)


def collect_bases(acc: Set[str], project_data: dict) -> Set[str]:
    return append_bricks(acc, "bases", project_data)


def collect_components(acc: Set[str], project_data: dict) -> Set[str]:
    return append_bricks(acc, "components", project_data)


if False:
    root = Path.cwd()
    ns = "polylith"

    projects_data = [p for p in info.get_projects_data(root, ns) if info.is_project(p)]

    bases: Set[str] = reduce(collect_bases, projects_data, set())
    components: Set[str] = reduce(collect_components, projects_data, set())

    # TODO: this is very strict, assuming all tests are structured as the "default"
    bases_tests = workspace.paths.collect_bases_tests_paths(root, ns, bases)
    components_tests = workspace.paths.collect_components_tests_paths(root, ns, components)
    tests = bases_tests.union(components_tests)

    # TODO: compare tests with changed tests

    brick_imports = get_brick_imports(root, ns, tests)

    get_projects_affected_by_changes(projects_data, brick_imports)
