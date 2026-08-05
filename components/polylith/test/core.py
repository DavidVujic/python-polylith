from pathlib import Path
from typing import List, Set, Union

from polylith import diff, imports


def is_test(root: Path, ns: str, path: Path, theme: str) -> bool:
    expected = "test"
    file_path = path.as_posix()

    if theme == "loose":
        test_path = Path(root / f"{expected}/").as_posix()

        return str.startswith(file_path, test_path)

    return f"/{expected}/{ns}" in file_path


def extract_parts_from_test_path(root: Path, path: Path) -> List[str]:
    relative_path = str.replace(path.as_posix(), root.as_posix(), "")
    parts = str.split(relative_path, "/")

    return [p for p in parts if p]


def extract_brick_type_from_test(root: Path, path: Path, theme: str) -> str:
    parts = extract_parts_from_test_path(root, path)

    return parts[1] if theme == "loose" else parts[0]


def extract_brick_name_from_test(root: Path, path: Path, theme: str) -> str:
    parts = extract_parts_from_test_path(root, path)

    return parts[3] if theme == "loose" else parts[1]


def find_tests(root: Path, ns: str, theme: str, files: List[Path]) -> Set[Path]:
    return {f for f in files if is_test(root, ns, f, theme)}


def get_changed_files(root: Path, tag_name: Union[str, None]) -> List[Path]:
    tag = diff.collect.get_latest_tag(root, tag_name) or tag_name

    if not tag:
        return []

    return [root / f for f in diff.collect.get_files(tag)]


def get_brick_imports_in_tests(
    root: Path, ns: str, theme: str, files: List[Path]
) -> dict:
    matched = find_tests(root, ns, theme, files)

    listed_imports = [imports.list_imports(m) for m in matched]

    all_imports = dict(enumerate(listed_imports))

    return imports.extract_brick_imports(all_imports, ns)


def get_related_brick(root: Path, path: Path, theme: str) -> dict:
    brick_name = extract_brick_name_from_test(root, path, theme)
    brick_type = extract_brick_type_from_test(root, path, theme)

    return {"name": brick_name, "type": brick_type}


def get_related_bricks(root: Path, ns: str, theme: str, files: List[Path]) -> dict:
    matched = find_tests(root, ns, theme, files)

    bricks = (get_related_brick(root, m, theme) for m in matched)

    bases = {b["name"] for b in bricks if b["type"] == "bases"}
    components = {b["name"] for b in bricks if b["type"] == "components"}

    return {"bases": bases, "components": components}
