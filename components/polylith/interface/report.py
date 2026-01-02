from pathlib import Path

from polylith import imports, workspace
from polylith.reporting import theme
from rich import box
from rich.console import Console
from rich.table import Table


def get_brick_data(root: Path, ns: str, brick: str, brick_type: str) -> dict:
    paths = {brick}

    if brick_type == "base":
        brick_path = workspace.paths.collect_bases_paths(root, ns, paths)
    else:
        brick_path = workspace.paths.collect_components_paths(root, ns, paths)

    brick_api = imports.fetch_api(brick_path)
    exposes = brick_api.get(brick) or set()

    return {
        "name": brick,
        "type": brick_type,
        "exposes": sorted(exposes),
    }


def get_brick_imports(root: Path, ns: str, bases: set, components: set) -> dict:
    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    in_bases = imports.fetch_all_imports(bases_paths)
    in_components = imports.fetch_all_imports(components_paths)

    return {
        "bases": imports.extract_brick_imports_with_namespaces(in_bases, ns),
        "components": imports.extract_brick_imports_with_namespaces(in_components, ns),
    }


def print_brick_interface(root: Path, ns: str, brick: str, bricks: dict) -> None:
    bases = bricks["bases"]
    tag = "base" if brick in bases else "comp"

    brick_data = get_brick_data(root, ns, brick, tag)
    exposes = brick_data["exposes"]

    console = Console(theme=theme.poly_theme)

    table = Table(box=box.SIMPLE_HEAD)
    table.add_column(f"[{tag}]{brick}[/] [data]brick interface[/]")

    for e in exposes:
        table.add_row(f"[data]{e}[/]")

    console.print(table, overflow="ellipsis")
