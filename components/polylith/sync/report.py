from rich.console import Console
from rich.theme import Theme

info_theme = Theme(
    {
        "data": "#999966",
        "proj": "#8A2BE2",
        "comp": "#32CD32",
        "base": "#6495ED",
    }
)


def print_summary(diff: dict):
    console = Console(theme=info_theme)

    name = diff["name"]
    bases = diff["bases"]
    components = diff["components"]

    anything_to_sync = bases or components

    header = (
        f":point_right: [proj]{name}[/]"
        if anything_to_sync
        else f":heavy_check_mark: [proj]{name}[/]"
    )

    console.print(header)

    for b in bases:
        console.print(f"adding [base]{b}[/] base to [proj]{name}[/]")

    for c in components:
        console.print(f"adding [comp]{c}[/] component to [proj]{name}[/]")

    if anything_to_sync:
        console.print("")
