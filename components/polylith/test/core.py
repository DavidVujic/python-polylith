from pathlib import Path
from typing import List, Union

from polylith import check, diff, imports


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

    listed_imports = [imports.list_imports(m) for m in matched]

    all_imports = {k: v for k, v in enumerate(listed_imports)}

    return check.grouping.extract_brick_imports(all_imports, ns)
