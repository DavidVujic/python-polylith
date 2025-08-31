from functools import reduce
from io import StringIO
from pathlib import Path
from typing import Tuple, cast

from polylith.reporting import theme
from rich.console import Console
from rich.table import Table

replacements = {"\u2714": "X", "\U0001F448": "<-", "\U0001F449": "->"}


def replace_char(data: str, pair: Tuple[str, str]) -> str:
    return str.replace(data, *pair)


def adjust(data: str) -> str:
    return reduce(replace_char, replacements.items(), data)


def write_to_file(data: str, options: dict, command: str) -> None:
    adjusted = adjust(data)

    output = options["output"]
    fullpath = f"{output}/{command}.txt"

    Path(output).mkdir(parents=True, exist_ok=True)
    Path(fullpath).write_text(adjusted)


def save_recorded(console: Console, options: dict, command: str) -> None:
    exported = console.export_text()

    write_to_file(exported, options, command)


def save(table: Table, options: dict, command: str) -> None:
    console = Console(theme=theme.poly_theme, width=1024, file=StringIO())

    console.print(table, overflow="ellipsis")

    f = cast(StringIO, console.file)
    exported = f.getvalue()

    write_to_file(exported, options, command)
