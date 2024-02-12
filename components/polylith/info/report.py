from typing import List

from polylith.reporting import theme
from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.table import Table


def brick_status(brick, bricks, command: str) -> str:
    emoji = theme.check_emoji if command == "info" else ":gear:"

    status = emoji if brick in bricks else "-"

    return f"[data]{status}[/]"


def is_project(project: dict) -> bool:
    return project["type"] == "project"


def printable_name(project: dict, short: bool) -> str:
    if is_project(project):
        template = "[proj]{name}[/]"
        name = project["name"]
    else:
        template = "[data]{name}[/]"
        name = "development"

    if short:
        return template.format(name="\n".join(name))

    return template.format(name=name)


def build_bricks_in_projects_table(
    projects_data: List[dict],
    bases: List[str],
    components: List[str],
    options: dict,
) -> Table:
    short = options.get("short", False)
    command = options.get("command", "info")

    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]brick[/]")

    proj_cols = [printable_name(project, short) for project in projects_data]

    for col in proj_cols:
        table.add_column(col, justify="center")

    for brick in sorted(components):
        statuses = [
            brick_status(brick, p.get("components"), command) for p in projects_data
        ]
        cols = [f"[comp]{brick}[/]"] + statuses

        table.add_row(*cols)

    for brick in sorted(bases):
        statuses = [brick_status(brick, p.get("bases"), command) for p in projects_data]
        cols = [f"[base]{brick}[/]"] + statuses

        table.add_row(*cols)

    return table


def print_table(table: Table) -> None:
    console = Console(theme=theme.poly_theme)

    console.print(table, overflow="ellipsis")


def print_compressed_view_for_bricks_in_projects(
    projects_data: List[dict], bases: List[str], components: List[str]
) -> None:
    options = {"short": True}
    table = build_bricks_in_projects_table(projects_data, bases, components, options)

    print_table(table)


def print_bricks_in_projects(
    projects_data: List[dict], bases: List[str], components: List[str]
) -> None:
    options = {"short": False}
    table = build_bricks_in_projects_table(projects_data, bases, components, options)

    print_table(table)


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
