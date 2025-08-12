from pathlib import Path
from typing import List, Set

from polylith import configuration, info, repo, sync
from polylith.reporting import theme
from rich.console import Console
from rich.padding import Padding
from rich.prompt import Confirm, Prompt

console = Console(theme=theme.poly_theme)


def create_added_brick_message(bricks: Set[str], tag: str, project_name: str) -> str:
    number_of_bricks = len(bricks)
    plural = "s" if number_of_bricks > 1 else ""

    if tag == "base":
        grammar = f"base{plural}"
    else:
        grammar = f"component{plural}"

    return f"[data]Added {number_of_bricks} [{tag}]{grammar}[/] to the [proj]{project_name}[/] project.[/]"


def confirmation(diff: dict, project_name: str) -> None:
    pad = (1, 0, 0, 0)

    if not diff:
        nothing_added_message = f"[data]No bricks added to [proj]{project_name}[/][/]."
        console.print(Padding(nothing_added_message, pad))

        return

    bases = diff["bases"]
    components = diff["components"]

    bases_message = create_added_brick_message(bases, "base", project_name)
    console.print(Padding(bases_message, pad))

    if len(components) == 0:
        return

    components_message = create_added_brick_message(components, "comp", project_name)
    console.print(components_message)


def add_bricks_to_project(
    root: Path,
    ns: str,
    project_name: str,
    possible_bases: List[str],
) -> None:
    projects_data = info.get_projects_data(root, ns)
    project_data = next((p for p in projects_data if p["name"] == project_name), None)

    if not project_data:
        return

    message = f"[data]Project [proj]{project_name}[/] created.[/]"
    console.print(Padding(message, (0, 0, 1, 0)))

    first, *_ = possible_bases

    if not Confirm.ask(
        prompt=f"[data]Do you want to add bricks to the [proj]{project_name}[/] project?[/]",
        console=console,
    ):
        return

    question = "[data]What's the name of the Polylith [base]base[/] to add?[/]"

    base = Prompt.ask(
        prompt=question,
        console=console,
        default=first,
        show_default=True,
        case_sensitive=False,
    )

    all_bases = info.get_bases(root, ns)
    found_base = next((b for b in all_bases if str.lower(b) == str.lower(base)), None)

    if not found_base:
        confirmation({}, project_name)
        return

    diff = sync.calculate_needed_bricks(root, ns, project_data, found_base)

    sync.update_project(root, ns, diff)

    confirmation(diff, project_name)


def run(project_name: str) -> None:
    root = repo.get_workspace_root(Path.cwd())
    ns = configuration.get_namespace_from_config(root)

    possible_bases = sorted(info.find_unused_bases(root, ns))

    if not possible_bases:
        return

    add_bricks_to_project(root, ns, project_name, possible_bases)
