from functools import reduce
from itertools import zip_longest
from typing import List, Set, Tuple

from polylith.reporting import theme
from rich import box
from rich.console import Console
from rich.table import Table


def to_col(brick: str, tag: str) -> str:
    name = "\n".join(brick)

    return f"[{tag}]{name}[/]"


def brick_status(bricks: Set[str], brick_name: str, imported: str) -> str:
    status = theme.check_emoji if imported in bricks and imported != brick_name else "-"

    return f"[data]{status}[/]"


def to_row(name: str, tag: str, brick_imports: dict, imported: List[str]) -> List[str]:
    bricks = brick_imports.get(name) or set()
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


def without(key: str, bricks: Set[str]) -> Set[str]:
    return {b for b in bricks if b != key}


def sorted_usings(usings: Set[str], bases: Set[str], components: Set[str]) -> List[str]:
    usings_bases = sorted({b for b in usings if b in bases})
    usings_components = sorted({c for c in usings if c in components})

    return usings_components + usings_bases


def sorted_used_by(
    brick: str, bases: Set[str], components: Set[str], import_data: dict
) -> List[str]:
    brick_used_by = without(brick, {k for k, v in import_data.items() if brick in v})

    return sorted_usings(brick_used_by, bases, components)


def sorted_uses(
    brick: str, bases: Set[str], components: Set[str], import_data: dict
) -> List[str]:
    brick_uses = without(brick, {b for b in import_data[brick]})

    return sorted_usings(brick_uses, bases, components)


def calculate_tag(brick: str, bases: Set[str]) -> str:
    return "base" if brick in bases else "comp"


def print_brick_deps(
    brick: str, bases: Set[str], components: Set[str], import_data: dict
):
    brick_used_by = sorted_used_by(brick, bases, components, import_data)
    brick_uses = sorted_uses(brick, bases, components, import_data)

    tag = calculate_tag(brick, bases)

    console = Console(theme=theme.poly_theme)

    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]used by[/]")
    table.add_column(":backhand_index_pointing_left:")
    table.add_column(f"[{tag}]{brick}[/]")
    table.add_column(":backhand_index_pointing_right:")
    table.add_column("[data]uses[/]")

    for item in zip_longest(brick_used_by, brick_uses):
        used_by, uses = item

        used_by_tag = calculate_tag(used_by, bases) if used_by else ""
        uses_tag = calculate_tag(uses, bases) if uses else ""

        left = f"[{used_by_tag}]{used_by}[/]" if used_by else ""
        right = f"[{uses_tag}]{uses}[/]" if uses else ""

        row = [left, "", "", "", right]

        table.add_row(*row)

    console.print(table, overflow="ellipsis")
