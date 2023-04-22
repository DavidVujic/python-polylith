from typing import List

from polylith.reporting import theme
from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.padding import Padding
from rich.table import Table


def brick_status(brick, bricks) -> str:
    status = ":gear:" if brick in bricks else "-"

    return f"[data]{status}[/]"


def print_diff_details(
    projects_data: List[dict], bases: List[str], components: List[str]
) -> None:

    if not bases and not components:
        return

    console = Console(theme=theme.poly_theme)
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]changed brick[/]")

    proj_cols = [f"[proj]{project['name']}[/]" for project in projects_data]
    table.add_column(Columns(proj_cols, align="center", expand=True))

    for brick in sorted(components):
        cols = [brick_status(brick, p.get("components")) for p in projects_data]
        table.add_row(f"[comp]{brick}[/]", Columns(cols, align="center", expand=True))

    for brick in sorted(bases):
        cols = [brick_status(brick, p.get("bases")) for p in projects_data]
        table.add_row(f"[base]{brick}[/]", Columns(cols, align="center", expand=True))

    console.print(table, overflow="ellipsis")


def print_detected_changes_in_projects(projects: List[str]) -> None:
    if not projects:
        return

    console = Console(theme=theme.poly_theme)

    for project in sorted(projects):
        console.print(f"[data]:gear: Changes found in [/][proj]{project}[/]")


def print_diff_summary(tag: str, bases: List[str], components: List[str]) -> None:
    console = Console(theme=theme.poly_theme)

    console.print(Padding(f"[data]Diff: based on the {tag} tag[/]", (1, 0, 1, 0)))

    if not bases and not components:
        console.print("[data]No brick changes found.[/]")
        return

    if components:
        console.print(f"[comp]Changed components[/]: [data]{len(components)}[/]")

    if bases:
        console.print(f"[base]Changed bases[/]: [data]{len(bases)}[/]")


def _changed_projects(
    projects_data: List[dict], brick_type: str, bricks: List[str]
) -> set:
    res = {
        p["path"].name: set(p.get(brick_type, [])).intersection(bricks)
        for p in projects_data
    }

    return {k for k, v in res.items() if v}


def print_short_diff(
    projects_data: List[dict],
    projects: List[str],
    bases: List[str],
    components: List[str],
) -> None:

    a = _changed_projects(projects_data, "components", components)
    b = _changed_projects(projects_data, "bases", bases)
    c = set(projects)

    res = {*a, *b, *c}

    console = Console(theme=theme.poly_theme)
    console.print(",".join(res))
