from typing import List

from polylith import info
from polylith.reporting import theme
from rich.console import Console
from rich.padding import Padding


def print_diff_details(
    projects_data: List[dict], bases: List[str], components: List[str]
) -> None:
    if not bases and not components:
        return

    console = Console(theme=theme.poly_theme)

    options = {"command": "diff"}
    table = info.report.build_bricks_in_projects_table(
        projects_data, bases, components, options
    )

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
