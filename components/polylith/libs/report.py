from pathlib import Path
from typing import List, Set

from polylith import info, libs, workspace


def get_projects_data(root: Path, ns: str) -> List[dict]:
    bases = info.get_bases(root, ns)
    components = info.get_components(root, ns)

    return info.get_bricks_in_projects(root, components, bases, ns)


def get_third_party_imports(
    root: Path, ns: str, projects_data: List[dict]
) -> dict[str, dict[str, Set]]:
    bases = {b for data in projects_data for b in data.get("bases", [])}
    components = {c for data in projects_data for c in data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    bases_imports = libs.get_third_party_imports(root, bases_paths)
    components_imports = libs.get_third_party_imports(root, components_paths)

    return {"bases": bases_imports, "components": components_imports}


def flatten_imports(brick_imports: dict[str, dict], brick: str) -> Set[str]:
    return set().union(*brick_imports.get(brick, {}).values())


def calculate_diff(
    brick_imports: dict[str, dict], third_party_libs: Set[str]
) -> Set[str]:
    bases_imports = flatten_imports(brick_imports, "bases")
    components_imports = flatten_imports(brick_imports, "components")

    return set().union(bases_imports, components_imports).difference(third_party_libs)
