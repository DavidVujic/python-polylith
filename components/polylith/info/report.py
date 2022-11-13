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
    projects_data: list[dict], bases_data: list[dict], components_data: list[dict]
) -> None:
    if not components_data and not bases_data:
        return

    console = Console(theme=info_theme)
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]brick[/]")

    for project in projects_data:
        project_name = project["name"]
        table.add_column(f"[proj]{project_name}[/]")

    components = sorted((c["name"] for c in components_data))
    bases = sorted((b["name"] for b in bases_data))

    for brick in components:
        cols = [brick_status(brick, p.get("components")) for p in projects_data]
        table.add_row(f"[comp]{brick}[/]", Columns(cols))

    for brick in bases:
        cols = [brick_status(brick, p.get("bases")) for p in projects_data]
        table.add_row(f"[base]{brick}[/]", Columns(cols))

    console.print(table, overflow="ellipsis")


def print_workspace_summary(
    projects_data: list[dict], bases_data: list[dict], components_data: list[dict]
) -> None:
    console = Console(theme=info_theme)

    console.print(Padding("[data]Workspace summary[/]", (1, 0, 1, 0)))

    number_of_projects = len(projects_data) if projects_data else 0
    number_of_components = len(components_data) if components_data else 0
    number_of_bases = len(bases_data) if bases_data else 0

    console.print(f"[proj]projects[/]: [data]{number_of_projects}[/]")
    console.print(f"[comp]components[/]: [data]{number_of_components}[/]")
    console.print(f"[base]bases[/]: [data]{number_of_bases}[/]")
