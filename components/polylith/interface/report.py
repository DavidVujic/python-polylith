from pathlib import Path
from typing import Set, Tuple

from polylith import imports, workspace
from polylith.reporting import theme
from rich.console import Console
from rich.table import Table
from rich.tree import Tree


def get_brick_interface(root: Path, ns: str, brick: str, bricks: dict) -> set:
    bases = bricks["bases"]
    paths = {brick}

    if brick in bases:
        brick_paths = workspace.paths.collect_bases_paths(root, ns, paths)
    else:
        brick_paths = workspace.paths.collect_components_paths(root, ns, paths)

    bricks_api = imports.fetch_api(brick_paths)

    brick_api = bricks_api.get(brick) or set()

    return {f"{ns}.{brick}.{a}" for a in brick_api}


def get_brick_imports(root: Path, ns: str, bases: set, components: set) -> dict:
    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    in_bases = imports.fetch_all_imports(bases_paths)
    in_components = imports.fetch_all_imports(components_paths)

    extracted_bases = imports.extract_brick_imports_with_namespaces(in_bases, ns)
    extracted_components = imports.extract_brick_imports_with_namespaces(
        in_components, ns
    )

    return {**extracted_bases, **extracted_components}


def to_imported_api(brick_imports: Set[str]) -> Set[str]:
    return {imports.parser.extract_api_part(b) for b in brick_imports}


def filter_by_brick(brick_imports: Set[str], brick: str, ns: str) -> Set[str]:
    brick_with_ns = f"{ns}.{brick}"

    return {b for b in brick_imports if str.startswith(b, brick_with_ns)}


def is_matching_namespace(using: str, endpoint: str) -> bool:
    return str.startswith(endpoint, using) or str.startswith(using, endpoint)


def is_within_namespace(using: str, brick_interface: Set[str]) -> bool:
    return any(is_matching_namespace(using, i) for i in brick_interface)


def check_usage(usings: Set[str], brick_interface: Set[str]) -> dict:
    return {u: is_within_namespace(u, brick_interface) for u in usings}


def check_brick_interface_usage(
    root: Path, ns: str, brick: str, bricks: dict
) -> Tuple[set, dict]:
    brick_interface = get_brick_interface(root, ns, brick, bricks)

    bases = bricks["bases"]
    components = bricks["components"]

    brick_imports = get_brick_imports(root, ns, bases, components)
    filtered = {k: filter_by_brick(v, brick, ns) for k, v in brick_imports.items()}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    comp_paths = workspace.paths.collect_components_paths(root, ns, components)
    paths = bases_paths.union(comp_paths)

    usage = {
        p.name: imports.fetch_brick_import_usages(
            p, frozenset(filtered.get(p.name, set()))
        )
        for p in paths
    }

    collected = {k: {*v, *filtered.get(k, set())} for k, v in usage.items()}

    res = {k: check_usage(v, brick_interface) for k, v in collected.items()}

    return brick_interface, res


def has_valid_usage(checked_usage: dict) -> bool:
    return all(v for v in checked_usage.values())


def print_brick_interface_usage(root: Path, ns: str, brick: str, bricks: dict) -> None:
    brick_interface, res = check_brick_interface_usage(root, ns, brick, bricks)

    invalid_usage = {k: v for k, v in res.items() if not has_valid_usage(v)}

    if not invalid_usage:
        return

    console = Console(theme=theme.poly_theme)

    interface_table = Table(box=None)
    tag = "base" if brick in bricks["bases"] else "comp"
    interface_tree = Tree(f"[{tag}]{brick}[/] [data]interface[/]")

    for endpoint in sorted(brick_interface):
        interface_tree.add(f"[data]{endpoint}[/]")

    interface_table.add_row(interface_tree)

    console.print(interface_table, overflow="ellipsis")

    table = Table(box=None)

    for using_brick, usages in invalid_usage.items():
        tag = "base" if using_brick in bricks["bases"] else "comp"
        tree = Tree(f"[{tag}]{using_brick}[/] [data]using[/]")
        usings = {k for k, v in usages.items() if v is False}

        for using in usings:
            tree.add(f"[data]{using}[/]")

        table.add_row(tree)

    console.print(table, overflow="ellipsis")
