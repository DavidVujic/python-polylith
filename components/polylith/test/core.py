from pathlib import Path
from typing import List, Set

from polylith import check, diff, info


def get_brick_imports(root: Path, ns: str, tests: Set[str]) -> dict:
    paths = {Path(t) for t in tests}
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


if False:
    tests = {"test/components/polylith/pdm"}
    root = Path.cwd()
    ns = "polylith"
    brick_imports = get_brick_imports(root, ns, tests)

    projects_data = [p for p in info.get_projects_data(root, ns) if info.is_project(p)]

    get_projects_affected_by_changes(projects_data, brick_imports)
