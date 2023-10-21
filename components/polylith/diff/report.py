from typing import List, Set

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


def print_detected_changes(changes: List[str], markup: str, short: bool) -> None:
    if not changes:
        return

    console = Console(theme=theme.poly_theme)

    if short:
        console.print(",".join(changes))
        return

    for brick in changes:
        console.print(f"[data]:gear: Changes found in [/][{markup}]{brick}[/]")


def print_detected_changes_in_bricks(
    bases: List[str], components: List[str], short: bool
) -> None:
    sorted_bases = sorted(bases)
    sorted_components = sorted(components)

    if short:
        print_detected_changes(sorted_components + sorted_bases, "data", short)
    else:
        print_detected_changes(sorted_components, "comp", short)
        print_detected_changes(sorted_bases, "base", short)


def print_detected_changes_in_projects(projects: List[str], short: bool) -> None:
    print_detected_changes(projects, "proj", short)


def print_projects_affected_by_changes(projects: Set[str], short: bool) -> None:
    sorted_projects = sorted(list(projects))

    print_detected_changes(sorted_projects, "proj", short)


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
