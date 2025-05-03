from typing import List, Set

from polylith import info
from polylith.reporting import theme
from rich.console import Console
from rich.padding import Padding


def print_report_summary(
    projects_data: List[dict], bases: Set[str], components: Set[str], tag: str
) -> None:
    console = Console(theme=theme.poly_theme)

    number_of_projects = len(projects_data)
    number_of_components = len(components)
    number_of_bases = len(bases)

    console.print(Padding("[data]Projects and bricks affected by changes in tests[/]", (1, 0, 0, 0)))
    console.print(Padding(f"[data]Test diff based on {tag}[/]", (0, 0, 1, 0)))

    console.print(f"[proj]Affected projects[/]: [data]{number_of_projects}[/]")
    console.print(f"[comp]Affected components[/]: [data]{number_of_components}[/]")
    console.print(f"[base]Affected bases[/]: [data]{number_of_bases}[/]")


def print_detected_changes(changes: List[str], options: dict):
    short = options.get("short", False)

    if not changes:
        return

    console = Console(theme=theme.poly_theme)

    if short:
        console.out(",".join(changes))
        return

    for item in changes:
        console.print(f"[data]:gear: Changes affecting [/][data]{item}[/]")


def print_projects_affected_by_changes(
    projects_data: List[dict], options: dict
) -> None:
    sorted_projects = [p["path"].name for p in projects_data]

    print_detected_changes(sorted_projects, options)


def print_detected_changes_affecting_bricks(
    bases: Set[str], components: Set[str], options: dict
) -> None:
    bricks = bases.union(components)
    changes = sorted(list(bricks))

    print_detected_changes(changes, options)


def print_test_report(
    projects_data: List[dict], bases: Set[str], components: Set[str], options: dict
) -> None:
    short = options.get("short", False)

    b = sorted(list(bases))
    c = sorted(list(components))

    if not b and not c:
        return

    if short:
        info.print_compressed_view_for_bricks_in_projects(projects_data, b, c)
    else:
        info.print_bricks_in_projects(projects_data, b, c)
