from pathlib import Path
from typing import List, Set

from polylith import check, configuration, diff, info


def get_projects_affected_by_changes(
    projects_data: List[dict], brick_imports: dict
) -> Set[str]:
    names = set().union(*brick_imports.values())
    bricks = list(names)

    return diff.collect.get_projects_affected_by_changes(
        projects_data, [], bricks, bricks
    )


def is_test(root: Path, ns: str, filepath: Path, theme: str) -> bool:
    if theme == "loose":
        test_path = root / "test"
        return str.startswith(filepath.as_posix(), test_path.as_posix())

    return f"/test/{ns}" in filepath.as_posix()


def comment():
    root = Path.cwd()
    ns = configuration.get_namespace_from_config(root)
    theme = configuration.get_theme_from_config(root)

    projects_data = [p for p in info.get_projects_data(root, ns) if info.is_project(p)]

    tag = diff.collect.get_latest_tag(root, None)
    files = [root / f for f in diff.collect.get_files(tag)]

    matched = {f for f in files if is_test(root, ns, f, theme)}

    brick_imports = check.collect.extract_bricks(matched, ns)

    get_projects_affected_by_changes(projects_data, brick_imports)
