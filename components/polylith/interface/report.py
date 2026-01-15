from pathlib import Path
from typing import Dict, FrozenSet, Set, Tuple

from polylith import imports
from polylith.reporting import theme
from polylith.workspace.paths import collect_bases_paths, collect_components_paths
from rich.console import Console
from rich.padding import Padding
from rich.table import Table


def get_brick_interface(root: Path, ns: str, brick: str, bricks: dict) -> set:
    bases = bricks["bases"]
    paths = {brick}

    fn = collect_bases_paths if brick in bases else collect_components_paths

    brick_paths = fn(root, ns, paths)
    bricks_api = imports.fetch_api(brick_paths)
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


def to_imported_api(brick_imports: Set[str]) -> Set[str]:
    return {imports.parser.extract_api_part(b) for b in brick_imports}


def filter_by_brick(brick_imports: Set[str], brick: str, ns: str) -> Set[str]:
    brick_with_ns = f"{ns}.{brick}"

    return {b for b in brick_imports if str.startswith(b, brick_with_ns)}


def is_within_namespace(current: str, namespaces: Set[str]) -> bool:
    return any(current.startswith(i) for i in namespaces)


def starts_with(usages: Set[str], current: str) -> bool:
    return any(usage.startswith(current + ".") for usage in usages)


def check_usage(usings: Set[str], brick_interface: Set[str]) -> dict:
    return {u: is_within_namespace(u, brick_interface) for u in usings}


def frozen(data: Dict[str, Set[str]], key: str) -> FrozenSet[str]:
    return frozenset(data.get(key) or set())


def check_brick_interface_usage(
    root: Path, ns: str, brick: str, bricks: dict
) -> Tuple[dict, set]:
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

    return checked, brick_interface


def print_brick_interface(brick: str, brick_interface: set, bricks: dict) -> None:
    console = Console(theme=theme.poly_theme)

    tag = "base" if brick in bricks["bases"] else "comp"

    table = Table(box=None)

    message = f"[{tag}]{brick}[/] exposes:"
    table.add_column(Padding(message, (1, 0, 0, 0)))

    for endpoint in sorted(brick_interface):
        *_ns, exposes = str.split(endpoint, ".")
        table.add_row(f"[data]{exposes}[/]")

    console.print(table, overflow="ellipsis")


def unified_usages(usages: dict) -> Set[str]:
    filtered = {k for k, v in usages.items() if not v}

    return {f for f in filtered if starts_with(filtered, f)}


def print_brick_interface_usage(root: Path, ns: str, brick: str, bricks: dict) -> None:
    res, brick_interface = check_brick_interface_usage(root, ns, brick, bricks)

    invalid_usage = {
        brick: unified_usages(usages)
        for brick, usages in res.items()
        if not all(usages.values())
    }

    if not invalid_usage:
        return

    console = Console(theme=theme.poly_theme)

    table = Table(box=None)
    tag = "base" if brick in bricks["bases"] else "comp"

    for using_brick, usages in invalid_usage.items():
        using_tag = "base" if using_brick in bricks["bases"] else "comp"

        for using in usages:
            used = str.replace(using, f"{ns}.{brick}.", "")
            prefix = f"Found in [{using_tag}]{using_brick}[/]"
            middle = f"[data]{used}[/] is not part of the public interface of [{tag}]{brick}[/]"

            message = f":information: {prefix}: {middle}."

            table.add_row(f"{message}")

    console.print(table, overflow="ellipsis")

    print_brick_interface(brick, brick_interface, bricks)
