from typing import List

from polylith.reporting import theme
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.padding import Padding
from rich.table import Table


def brick_status(brick, bricks) -> str:
    status = ":heavy_check_mark:" if brick in bricks else "-"

    return f"[data]{status}[/]"


def is_project(project: dict) -> bool:
    return project["type"] == "project"


def printable_name(project: dict) -> str:
    name = project["name"]

    if is_project(project):
        return f"[proj]{name}[/]"

    return "[data]development[/]"


def print_bricks_in_projects(
    projects_data: List[dict], bases: List[str], components: List[str]
) -> None:
    if not components and not bases:
        return

    console = Console(theme=theme.poly_theme)
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]brick[/]")

    proj_cols = [printable_name(project) for project in projects_data]
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
    console = Console(theme=theme.poly_theme)

    console.print(Padding("[data]Workspace summary[/]", (1, 0, 1, 0)))

    number_of_projects = len([p for p in projects_data if is_project(p)])
    number_of_components = len(components)
    number_of_bases = len(bases)
    number_of_dev = len([p for p in projects_data if not is_project(p)])

    console.print(f"[proj]projects[/]: [data]{number_of_projects}[/]")
    console.print(f"[comp]components[/]: [data]{number_of_components}[/]")
    console.print(f"[base]bases[/]: [data]{number_of_bases}[/]")
    console.print(f"[data]development[/]: [data]{number_of_dev}[/]")
