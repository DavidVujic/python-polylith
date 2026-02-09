from pathlib import Path

from polylith.interface.collect import get_brick_interface
from polylith.interface.usage import check_brick_interface_usage, unified_usages
from polylith.reporting import theme
from rich.console import Console
from rich.table import Table


def print_brick_interface(root: Path, ns: str, brick: str, bricks: dict) -> None:
    brick_interface = get_brick_interface(root, ns, brick, bricks)

    if not brick_interface:
        return

    console = Console(theme=theme.poly_theme)

    tag = "base" if brick in bricks["bases"] else "comp"

    table = Table(box=None)

    message = f"[{tag}]{brick}[/] exposes:"
    table.add_column(message)

    for endpoint in sorted(brick_interface):
        *_ns, exposes = str.split(endpoint, ".")
        table.add_row(f"[data]{exposes}[/]")

    console.print(table, overflow="ellipsis")


def print_brick_interface_invalid_usage(
    root: Path, ns: str, brick: str, bricks: dict
) -> None:
    res = check_brick_interface_usage(root, ns, brick, bricks)

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
