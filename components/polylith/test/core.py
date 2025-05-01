from pathlib import Path
from typing import List, Union

from polylith import check, configuration, diff, info
from polylith.bricks import get_bases_data, get_components_data


def is_test(root: Path, ns: str, path: Path, theme: str) -> bool:
    expected = "test"
    file_path = path.as_posix()

    if theme == "loose":
        test_path = Path(root / f"{expected}/").as_posix()

        return str.startswith(file_path, test_path)

    return f"/{expected}/{ns}" in file_path


def get_changed_files(root: Path, tag_name: Union[str, None]) -> List[Path]:
    tag = diff.collect.get_latest_tag(root, tag_name) or tag_name

    if not tag:
        return []

    return [root / f for f in diff.collect.get_files(tag)]


def get_brick_imports_in_tests(
    root: Path, ns: str, theme: str, files: List[Path]
) -> dict:
    matched = {f for f in files if is_test(root, ns, f, theme)}

    return check.collect.extract_bricks(matched, ns)


def comment():
    root = Path.cwd()
    ns = configuration.get_namespace_from_config(root)
    theme = configuration.get_theme_from_config(root)

    projects_data = [p for p in info.get_projects_data(root, ns) if info.is_project(p)]

    files = get_changed_files(root, None)
    brick_imports = get_brick_imports_in_tests(root, ns, theme, files)
    bricks = set().union(*brick_imports.values())

    all_bases = {v for b in get_bases_data(root, ns) for v in b.values()}
    all_components = {v for c in get_components_data(root, ns) for v in c.values()}

    bases = [b for b in all_bases if b in bricks]
    components = [c for c in all_components if c in bricks]

    diff.collect.get_projects_affected_by_changes(projects_data, [], bases, components)
