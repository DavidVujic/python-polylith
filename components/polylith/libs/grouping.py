import sys
from pathlib import Path
from typing import List, Set

from polylith import repo, workspace
from polylith.libs.imports import list_imports
from polylith.libs.stdlib import standard_libs


def get_python_version() -> str:
    return f"{sys.version_info.major}.{sys.version_info.minor}"


def get_standard_libs(python_version: str) -> Set[str]:
    return standard_libs.get(python_version, set())


def fetch_all_imports(paths: List[Path]) -> Set[str]:
    res = (list_imports(p) for p in paths)

    return set().union(*res)


def extract_top_ns(imp: str) -> str:
    res = imp.split(".")

    return res[0]


def extract_top_ns_from_all_imports(paths: List[Path]) -> Set[str]:
    all_imports = fetch_all_imports(paths)

    return {extract_top_ns(imp) for imp in all_imports}


def get_all_third_party_imports() -> Set[str]:
    root = repo.find_workspace_root(Path.cwd())

    if not root:
        raise ValueError("Could not find the repo root")

    components_dir = root / "components"
    bases_dir = root / "bases"

    python_version = get_python_version()
    std_libs = get_standard_libs(python_version)
    top_ns = workspace.parser.get_namespace_from_config(root)

    imports = extract_top_ns_from_all_imports([components_dir, bases_dir])

    return imports - std_libs.union({top_ns})
