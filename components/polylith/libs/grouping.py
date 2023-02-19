import sys
from pathlib import Path
from typing import Set

from polylith import workspace
from polylith.libs.imports import list_imports
from polylith.libs.stdlib import standard_libs


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def get_standard_libs(python_version: str) -> Set[str]:
    return standard_libs.get(python_version, set())


def fetch_all_imports(paths: Set[Path]) -> dict:
    rows = [{p.name: list_imports(p)} for p in paths]

    return {k: v for row in rows for k, v in row.items()}


def extract_top_ns_from_imports(imports: Set[str]) -> Set:
    return {imp.split(".")[0] for imp in imports}


def extract_top_ns(import_data: dict) -> dict:
    return {k: extract_top_ns_from_imports(v) for k, v in import_data.items()}


def exclude_libs(import_data: dict, to_exclude: Set) -> dict:
    return {k: v - to_exclude for k, v in import_data.items()}


def exclude_empty(import_data: dict) -> dict:
    return {k: v for k, v in import_data.items() if v}


def get_third_party_imports(root: Path, paths: Set[Path]) -> dict:
    python_version = get_python_version()
    std_libs = get_standard_libs(python_version)
    top_ns = workspace.parser.get_namespace_from_config(root)

    all_imports = fetch_all_imports(paths)
    top_level_imports = extract_top_ns(all_imports)

    with_third_party = exclude_libs(top_level_imports, std_libs.union({top_ns}))

    return exclude_empty(with_third_party)
