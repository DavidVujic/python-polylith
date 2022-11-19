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
    status = ":heavy_check_mark:" if brick in bricks else "-"

    return f"[data]{status}[/]"


def print_bricks_in_projects(
    projects_data: List[dict], bases: List[str], components: List[str]
) -> None:
    if not components and not bases:
        return

    console = Console(theme=info_theme)
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]brick[/]")

    proj_cols = [f"[proj]{project['name']}[/]" for project in projects_data]
    table.add_column(Columns(proj_cols, align="center", expand=True))

    for brick in sorted(components):
        cols = [brick_status(brick, p.get("components")) for p in projects_data]
        table.add_row(f"[comp]{brick}[/]", Columns(cols, align="center", expand=True))

    for brick in sorted(bases):
        cols = [brick_status(brick, p.get("bases")) for p in projects_data]
        table.add_row(f"[base]{brick}[/]", Columns(cols, align="center", expand=True))

    console.print(table, overflow="ellipsis")


def print_workspace_summary(
    projects_data: List[dict], bases: List[str], components: List[str]
) -> None:
    console = Console(theme=info_theme)

    console.print(Padding("[data]Workspace summary[/]", (1, 0, 1, 0)))

    number_of_projects = len(projects_data)
    number_of_components = len(components)
    number_of_bases = len(bases)

    console.print(f"[proj]projects[/]: [data]{number_of_projects}[/]")
    console.print(f"[comp]components[/]: [data]{number_of_components}[/]")
    console.print(f"[base]bases[/]: [data]{number_of_bases}[/]")
