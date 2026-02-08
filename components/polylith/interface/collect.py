from pathlib import Path

from polylith import imports
from polylith.interface.parser import fetch_api
from polylith.workspace.paths import collect_bases_paths, collect_components_paths


def get_brick_interface(root: Path, ns: str, brick: str, bricks: dict) -> set:
    bases = bricks["bases"]
    paths = {brick}

    fn = collect_bases_paths if brick in bases else collect_components_paths

    brick_paths = fn(root, ns, paths)
    bricks_api = fetch_api(brick_paths)
    brick_api = bricks_api.get(brick) or set()
    brick_ns = f"{ns}.{brick}"

    return {f"{brick_ns}.{endpoint}" for endpoint in brick_api}


def get_brick_imports(root: Path, ns: str, bases: set, components: set) -> dict:
    bases_paths = collect_bases_paths(root, ns, bases)
    components_paths = collect_components_paths(root, ns, components)

    in_bases = imports.fetch_all_imports(bases_paths)
    in_comps = imports.fetch_all_imports(components_paths)

    extracted_bases = imports.extract_brick_imports_with_namespaces(in_bases, ns)
    extracted_components = imports.extract_brick_imports_with_namespaces(in_comps, ns)

    return {**extracted_bases, **extracted_components}
