from polylith import check
from polylith.reporting import theme
from rich.console import Console


def print_brick_imports(diff: dict) -> None:
    brick_imports = diff["brick_imports"]

    check.report.print_brick_imports(brick_imports)


def print_summary(diff: dict) -> None:
    console = Console(theme=theme.poly_theme)

    is_project = diff["is_project"]
    name = diff["name"] if is_project else "development"
    bases = diff["bases"]
    components = diff["components"]

    anything_to_sync = bases or components

    emoji = ":point_right:" if anything_to_sync else theme.check_emoji
    printable_name = f"[proj]{name}[/]" if is_project else f"[data]{name}[/]"

    console.print(f"{emoji} {printable_name}")

    for b in bases:
        console.print(f"adding [base]{b}[/] base to [proj]{name}[/]")

    for c in components:
        console.print(f"adding [comp]{c}[/] component to [proj]{name}[/]")

    if anything_to_sync:
        console.print("")
