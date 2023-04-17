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

    project_name = diff["name"]

    console.print(f"Synchronizing [proj]{project_name}[/]")
