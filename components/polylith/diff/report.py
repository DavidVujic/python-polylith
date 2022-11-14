from typing import List

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.padding import Padding
from rich.table import Table
from rich.theme import Theme

info_theme = Theme(
    {
        "data": "#999966",
        "proj": "#8A2BE2",
        "comp": "#32CD32",
        "base": "#6495ED",
    }
)


def brick_status(brick, bricks) -> str:
    status = ":gear:" if brick in bricks else "-"

    return f"[data]{status}[/]"


def print_diff_details(
    projects_data: List[dict], bases: List[str], components: List[str]
) -> None:
    console = Console(theme=info_theme)
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]changed brick[/]")

    for project in projects_data:
        project_name = project["name"]
        table.add_column(f"[proj]{project_name}[/]")

    for brick in sorted(components):
        cols = [brick_status(brick, p.get("components")) for p in projects_data]
        table.add_row(f"[comp]{brick}[/]", Columns(cols))

    for brick in sorted(bases):
        cols = [brick_status(brick, p.get("bases")) for p in projects_data]
        table.add_row(f"[base]{brick}[/]", Columns(cols))

    console.print(table, overflow="ellipsis")


def print_detected_changes_in_projects(projects: List[str]) -> None:
    if not projects:
        return

    console = Console(theme=info_theme)

    for project in sorted(projects):
        console.print(f"[data]:gear: Changes found in [/][proj]{project}[/]")


def print_diff_summary(tag: str, bases: List[str], components: List[str]) -> None:
    console = Console(theme=info_theme)

    console.print(Padding(f"[data]Diff: based on the {tag} tag[/]", (1, 0, 1, 0)))

    if not bases and not components:
        console.print("[data]No brick changes found.[/]")
        return

    if components:
        console.print(f"[comp]Changed components[/]: [data]{len(components)}[/]")

    if bases:
        console.print(f"[base]Changed bases[/]: [data]{len(bases)}[/]")
