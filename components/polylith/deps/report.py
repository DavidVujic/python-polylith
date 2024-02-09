from typing import List

from polylith.reporting import theme
from rich import box
from rich.console import Console
from rich.table import Table


def brick_status(brick_imports: dict, brick_name: str, imported: str) -> str:
    bricks = brick_imports[brick_name]

    if brick_name == imported:
        status = ""
    elif imported in bricks:
        status = ":heavy_check_mark:"
    else:
        status = "-"

    return f"[data]{status}[/]"


def calculate_tag(brick: str, project_data: dict) -> str:
    return "base" if brick in project_data.get("bases", []) else "comp"


def extract_names(project_data: dict) -> List[str]:
    bases = project_data.get("bases", [])
    components = project_data.get("components", [])

    return sorted(components) + sorted(bases)


def print_deps(project_data: dict, brick_imports: dict):
    brick_names = extract_names(project_data)
    flattened_imports = sorted(set().union(*brick_imports.values()))

    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]brick[/]")

    for imported in flattened_imports:
        tag = calculate_tag(imported, project_data)
        name = "\n".join(imported)

        table.add_column(f"[{tag}]{name}[/]", justify="center")

    for name in brick_names:
        tag = calculate_tag(name, project_data)
        statuses = [brick_status(brick_imports, name, i) for i in flattened_imports]
        cols = [f"[{tag}]{name}[/]"] + statuses

        table.add_row(*cols)

    console = Console(theme=theme.poly_theme)

    console.print(table, overflow="ellipsis")
