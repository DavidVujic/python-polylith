from pathlib import Path
from typing import Set

from polylith import workspace
from polylith.libs.imports import list_imports


def fetch_all_imports(paths: Set[Path]) -> dict:
    rows = [{p.name: list_imports(p)} for p in paths]

    return {k: v for row in rows for k, v in row.items()}


def extract_top_ns_from_imports(imports: Set[str]) -> Set:
    return {imp.split(".")[0] for imp in imports}


def extract_top_ns(import_data: dict) -> dict:
    return {k: extract_top_ns_from_imports(v) for k, v in import_data.items()}


def only_brick_imports(imports: Set[str], top_ns: str) -> Set[str]:
    return {i for i in imports if i.startswith(top_ns)}


def only_bricks(import_data: dict, top_ns: str) -> dict:
    return {k: only_brick_imports(v, top_ns) for k, v in import_data.items()}


def brick_import_to_name(brick_import: str) -> str:
    parts = brick_import.split(".")

    return f"{parts[0]}.{parts[1]}" if len(parts) > 1 else brick_import


def only_brick_name(brick_imports: Set[str]) -> Set[str]:
    return {brick_import_to_name(i) for i in brick_imports}


def only_brick_names(import_data: dict) -> dict:
    return {k: only_brick_name(v) for k, v in import_data.items() if v}


def exclude_empty(import_data: dict) -> dict:
    return {k: v for k, v in import_data.items() if v}


def get_brick_imports(root: Path, paths: Set[Path]) -> dict:
    top_ns = workspace.parser.get_namespace_from_config(root)

    all_imports = fetch_all_imports(paths)

    with_only_bricks = only_bricks(all_imports, top_ns)
    with_only_brick_names = only_brick_names(with_only_bricks)

    return exclude_empty(with_only_brick_names)
