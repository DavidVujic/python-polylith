from typing import List, Set

from polylith import diff
from polylith.reporting import theme
from rich.console import Console
from rich.padding import Padding


def print_projects_affected_by_changes(projects: Set[str], short: bool) -> None:
    diff.report.print_projects_affected_by_changes(projects, short)


def print_diff_summary(tag: str, bases: List[str], components: List[str]) -> None:
    console = Console(theme=theme.poly_theme)

    console.print(Padding(f"[data]Diff: based on {tag}[/]", (1, 0, 1, 0)))

    if not bases and not components:
        console.print("[data]No changes affecting bricks found.[/]")
        return

    if components:
        console.print(
            f"[comp]Components in changed tests[/]: [data]{len(components)}[/]"
        )

    if bases:
        console.print(f"[base]Bases in changed tests[/]: [data]{len(bases)}[/]")


def print_detected_changes_affecting_bricks(
    bases: Set[str], components: Set[str], options: dict
) -> None:
    bricks = bases.union(components)
    changes = sorted(list(bricks))

    short = options.get("short", False)
    query = options.get("query", False)

    if not changes:
        return

    console = Console(theme=theme.poly_theme)

    if short:
        console.out(",".join(changes))
        return

    if query:
        console.out(" or ".join(changes))
        return

    for brick in changes:
        console.print(f"[data]:gear: Changes in test using: [/][data]{brick}[/]")
