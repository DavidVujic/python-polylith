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


def calculate_print_friendly_brick_type(bricks: List[str], markup: str) -> str:
    plural = len(bricks) > 1

    if markup == "base":
        return "bases" if plural else "base"

    return "components" if plural else "component"


def print_detected_dependent(bricks: List[str], markup: str) -> None:
    if not bricks:
        return

    console = Console(theme=theme.poly_theme)

    brick_type = calculate_print_friendly_brick_type(bricks, markup)
    printable_bricks = [f"[{markup}]{b}[/]" for b in bricks]
    joined = ", ".join(printable_bricks)

    console.print(f"[data]:gear: Dependent {brick_type}: [/]{joined}")


def print_detected_changes_in_bricks(
    changed_bases: List[str],
    changed_components: List[str],
    dependent_bricks: dict,
    options: dict,
) -> None:
    short = options.get("short", False)
    bases = sorted(changed_bases)
    components = sorted(changed_components)

    dependent_bases = sorted(dependent_bricks.get("bases", []))
    dependent_components = sorted(dependent_bricks.get("components", []))

    if short:
        bricks = components + bases + dependent_components + dependent_bases
        print_detected_changes(bricks, "data", short)
    else:
        print_detected_changes(components, "comp", short)
        print_detected_changes(bases, "base", short)
        print_detected_dependent(dependent_components, "comp")
        print_detected_dependent(dependent_bases, "base")


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
