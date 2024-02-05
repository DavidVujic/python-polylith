import sys
from pathlib import Path
from typing import Set

from polylith import configuration
from polylith.imports import extract_top_ns, fetch_all_imports
from polylith.libs.stdlib import standard_libs


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def get_latest_standard_libs() -> Set[str]:
    values = list(standard_libs.values())

    return values[-1]


def get_standard_libs(python_version: str) -> Set[str]:
    libs = standard_libs.get(python_version)

    return libs or get_latest_standard_libs()


def exclude_libs(import_data: dict, to_exclude: Set) -> dict:
    return {k: v - to_exclude for k, v in import_data.items()}


def exclude_empty(import_data: dict) -> dict:
    return {k: v for k, v in import_data.items() if v}


def extract_third_party_imports(all_imports: dict, top_ns: str) -> dict:
    python_version = get_python_version()
    std_libs = get_standard_libs(python_version)

    top_level_imports = extract_top_ns(all_imports)
    with_third_party = exclude_libs(top_level_imports, std_libs.union({top_ns}))

    return exclude_empty(with_third_party)


def get_third_party_imports(root: Path, paths: Set[Path]) -> dict:
    top_ns = configuration.get_namespace_from_config(root)

    all_imports = fetch_all_imports(paths)

    return extract_third_party_imports(all_imports, top_ns)
