from pathlib import Path
from typing import Dict, FrozenSet, Set

from polylith import imports
from polylith.interface.collect import get_brick_imports, get_brick_interface
from polylith.workspace.paths import collect_bases_paths, collect_components_paths


def extract_endpoint(usage: str) -> str:
    separator = "."

    if separator not in usage:
        return usage

    ns, brick, *rest = str.split(usage, separator)

    return rest[0]


def unified_usages(usages: dict) -> Set[str]:
    filtered = {k for k, v in usages.items() if not v}

    return {extract_endpoint(f) for f in filtered}


def to_imported_api(brick_imports: Set[str]) -> Set[str]:
    return {imports.usages.extract_api_part(b) for b in brick_imports}


def filter_by_brick(brick_imports: Set[str], brick: str, ns: str) -> Set[str]:
    brick_with_ns = f"{ns}.{brick}"

    return {b for b in brick_imports if str.startswith(b, brick_with_ns)}


def is_within_namespace(current: str, namespaces: Set[str]) -> bool:
    return any(current.startswith(i) for i in namespaces)


def check_usage(usings: Set[str], brick_interface: Set[str]) -> dict:
    return {u: is_within_namespace(u, brick_interface) for u in usings}


def frozen(data: Dict[str, Set[str]], key: str) -> FrozenSet[str]:
    return frozenset(data.get(key) or set())


def check_brick_interface_usage(root: Path, ns: str, brick: str, bricks: dict) -> dict:
    brick_interface = get_brick_interface(root, ns, brick, bricks)
    bases = bricks["bases"]
    components = bricks["components"]

    brick_imports = get_brick_imports(root, ns, bases, components)
    by_brick = {k: filter_by_brick(v, brick, ns) for k, v in brick_imports.items()}

    bases_paths = collect_bases_paths(root, ns, bases)
    comp_paths = collect_components_paths(root, ns, components)
    paths = bases_paths.union(comp_paths)

    usage = {
        p.name: imports.fetch_brick_import_usages(p, ns, frozen(by_brick, p.name))
        for p in paths
    }

    checked = {k: check_usage(v, brick_interface) for k, v in usage.items()}

    return checked
