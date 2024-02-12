from pathlib import Path
from typing import List, Union

from polylith import bricks, deps, info


def print_report(root: Path, ns: str, bases: List[str], components: List[str]):
    brick_imports = deps.get_brick_imports(root, ns, bases, components)

    flattened = {**brick_imports["bases"], **brick_imports["components"]}

    deps.print_deps(bases, components, flattened)


def run(root: Path, ns: str, directory: Union[str, None]):
    ws_bases = [b["name"] for b in bricks.get_bases_data(root, ns)]
    ws_components = [c["name"] for c in bricks.get_components_data(root, ns)]

    projects_data = info.get_projects_data(root, ns) if directory else []
    proj_data = next((p for p in projects_data if directory in p["path"].as_posix()), {})

    proj_bases = proj_data.get("bases", {}) if proj_data else ws_bases
    proj_components = proj_data.get("components", {}) if proj_data else ws_components

    bases = [b for b in ws_bases if b in proj_bases]
    components = [c for c in ws_components if c in proj_components]

    print_report(root, ns, bases, components)
