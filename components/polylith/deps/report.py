from functools import reduce
from typing import List, Set, Tuple

from polylith.reporting import theme
from rich import box
from rich.console import Console
from rich.table import Table


def calculate_tag(brick: str, project_data: dict) -> str:
    return "base" if brick in project_data.get("bases", []) else "comp"


def to_col(brick: str, tag: str) -> str:
    name = "\n".join(brick)

    return f"[{tag}]{name}[/]"


def brick_status(bricks: List[str], brick_name: str, imported: str) -> str:
    status = theme.check_emoji if imported in bricks and imported != brick_name else "-"

    return f"[data]{status}[/]"


def to_row(name: str, tag: str, brick_imports: dict, imported: List[str]) -> List[str]:
    bricks = brick_imports[name]
    statuses = [brick_status(bricks, name, i) for i in imported]

    return [f"[{tag}]{name}[/]"] + statuses


def flatten_import(acc: Set[str], kv: Tuple[str, Set[str]]) -> set:
    key = kv[0]
    values = kv[1]

    return set().union(acc, values.difference({key}))


def flatten_imports(brick_imports: dict) -> Set[str]:
    """Flatten the dict into a set of imports, with the actual brick filtered away when existing as an import"""
    return reduce(flatten_import, brick_imports.items(), set())


def create_columns(
    imported_bases: List[str], imported_components: List[str]
) -> List[str]:
    base_cols = [to_col(brick, "base") for brick in imported_bases]
    comp_cols = [to_col(brick, "comp") for brick in imported_components]

    return comp_cols + base_cols


def create_rows(
    bases: Set[str], components: Set[str], import_data: dict, imported: List[str]
) -> List[List[str]]:
    base_rows = [to_row(b, "base", import_data, imported) for b in sorted(bases)]
    comp_rows = [to_row(c, "comp", import_data, imported) for c in sorted(components)]

    return comp_rows + base_rows


def print_deps(bases: Set[str], components: Set[str], import_data: dict):
    flattened = flatten_imports(import_data)

    imported_bases = sorted({b for b in flattened if b in bases})
    imported_components = sorted({c for c in flattened if c in components})
    imported_bricks = imported_components + imported_bases

    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]brick[/]")

    cols = create_columns(imported_bases, imported_components)
    rows = create_rows(bases, components, import_data, imported_bricks)

    for col in cols:
        table.add_column(col, justify="center")

    for row in rows:
        table.add_row(*row)

    console = Console(theme=theme.poly_theme)

    console.print(table, overflow="ellipsis")
