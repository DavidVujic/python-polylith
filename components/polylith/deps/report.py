from polylith.reporting import theme
from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.table import Table


def print_table(table: Table) -> None:
    console = Console(theme=theme.poly_theme)

    console.print(table, overflow="ellipsis")


def print_brick_deps(brick_imports: dict):
    bases = brick_imports["bases"]
    components = brick_imports["components"]

    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]brick[/]")

"""
data = {
    "bases": {
        "pdm_project_hooks": {"pdm"},
        "pdm": {"configuration", "parsing", "pdm", "toml"},
        "configuration": {"configuration", "repo"},
        "toml": {"repo", "toml"},
        "parsing": {"parsing"},
        "repo": {"repo"},
    },
    "components": {
        "repo": {"repo"},
        "pdm": {"configuration", "parsing", "pdm", "toml"},
        "configuration": {"configuration", "repo"},
        "toml": {"repo", "toml"},
        "parsing": {"parsing"},
    },
}

c = data["components"]

from functools import reduce
from typing import Set


rows = set(c.keys())
cols: Set[str] = reduce(lambda acc, total: set().union(acc, total), c.values(), set())
"""
