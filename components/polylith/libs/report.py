from pathlib import Path
from typing import List, Set

from polylith import workspace
from polylith.libs import grouping


def get_third_party_imports(
    root: Path, ns: str, projects_data: List[dict]
) -> dict[str, dict]:
    bases = {b for data in projects_data for b in data.get("bases", [])}
    components = {c for data in projects_data for c in data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    bases_imports = grouping.get_third_party_imports(root, bases_paths)
    components_imports = grouping.get_third_party_imports(root, components_paths)

    return {"bases": bases_imports, "components": components_imports}


def flatten_imports(brick_imports: dict, brick: str) -> Set[str]:
    return set().union(*brick_imports.get(brick, {}).values())


def calculate_diff(brick_imports: dict, third_party_libs: Set[str]) -> Set[str]:
    bases_imports = flatten_imports(brick_imports, "bases")
    components_imports = flatten_imports(brick_imports, "components")

    return set().union(bases_imports, components_imports).difference(third_party_libs)
