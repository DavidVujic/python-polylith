from functools import reduce
from pathlib import Path
from typing import Tuple

from rich.console import Console

replacements = {"\u2714": "X", "\U0001F448": "<", "\U0001F449": ">"}


def replace_char(data: str, pair: Tuple[str, str]) -> str:
    return str.replace(data, *pair)


def adjust(data: str) -> str:
    return reduce(replace_char, replacements.items(), data)


def save(console: Console, options: dict, command: str) -> None:
    exported = console.export_text()
    adjusted = adjust(exported)

    output = options["output"]
    fullpath = f"{output}/{command}.txt"

    Path(output).mkdir(parents=True, exist_ok=True)
    Path(fullpath).write_text(adjusted)
