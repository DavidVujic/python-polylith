import sys
from typing import Set
from pathlib import Path

from polylith import repo, workspace
from polylith.libs.stdlib import standard_libs
from polylith.libs.imports import list_imports


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def get_standard_libs(python_version: str) -> Set[str]:
    return standard_libs.get(python_version, set())


def get_all_imports(root: Path) -> Set[str]:
    components_dir = root / "components"
    bases_dir = root / "bases"

    a = list_imports(components_dir)
    b = list_imports(bases_dir)

    return a.union(b)


def extract_top_ns(imp: str) -> str:
    res = imp.split(".")

    return res[0]


def extract_top_ns_from_all_imports(root: Path) -> Set[str]:
    all_imports = get_all_imports(root)

    return {extract_top_ns(imp) for imp in all_imports}


def get_all_third_party_imports() -> Set[str]:
    root = repo.find_workspace_root(Path.cwd())

    if not root:
        raise ValueError("Could not find the repo root")

    python_version = get_python_version()
    std_libs = get_standard_libs(python_version)
    top_ns = workspace.parser.get_namespace_from_config(root)

    imports = extract_top_ns_from_all_imports(root)

    return imports - std_libs.union({top_ns})
