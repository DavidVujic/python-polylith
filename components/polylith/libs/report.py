from pathlib import Path
from typing import Set

from polylith import workspace
from polylith.libs import grouping
from rich import box
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


def get_third_party_imports(root: Path, ns: str, project_data: dict) -> dict:
    bases = {b for b in project_data.get("bases", [])}
    components = {c for c in project_data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    bases_imports = grouping.get_third_party_imports(root, bases_paths)
    components_imports = grouping.get_third_party_imports(root, components_paths)

    return {"bases": bases_imports, "components": components_imports}


def flatten_imports(brick_imports: dict, brick: str) -> Set[str]:
    return set().union(*brick_imports.get(brick, {}).values())


def calculate_diff(brick_imports: dict, third_party_libs: Set[str]) -> Set[str]:
    bases_imports = flatten_imports(brick_imports, "bases")
    components_imports = flatten_imports(brick_imports, "components")

    return set().union(bases_imports, components_imports).difference(third_party_libs)


def print_libs_summary(brick_imports: dict, project_name: str) -> None:
    console = Console(theme=info_theme)

    console.print(
        Padding(f"[data]Libraries summary for [/][proj]{project_name}[/]", (1, 0, 1, 0))
    )

    bases_imports = flatten_imports(brick_imports, "bases")
    components_imports = flatten_imports(brick_imports, "components")

    console.print(f"[base]Libraries used in bases[/]: [data]{len(bases_imports)}[/]")
    console.print(
        f"[comp]libraries used in components[/]: [data]{len(components_imports)}[/]"
    )


def print_libs_in_bricks(brick_imports: dict) -> None:
    console = Console(theme=info_theme)
    table = Table(box=box.SIMPLE_HEAD)
    table.add_column("[data]brick[/]")
    table.add_column("[data]libraries[/]")

    bases = brick_imports.get("bases", {})
    components = brick_imports.get("components", {})

    for brick, imports in bases.items():
        table.add_row(f"[base]{brick}[/]", ", ".join(sorted(imports)))

    for brick, imports in components.items():
        table.add_row(f"[comp]{brick}[/]", ", ".join(sorted(imports)))

    console.print(table, overflow="ellipsis")


def print_missing_installed_libs(
    brick_imports: dict, third_party_libs: Set[str], project_data: dict
) -> None:
    diff = calculate_diff(brick_imports, third_party_libs)

    if not diff:
        return

    console = Console(theme=info_theme)

    project_name = project_data["name"]
    missing = ", ".join(sorted(diff))

    console.print(
        f"[data]Could not locate all libraries in [/][proj]{project_name}[/]. [data]Caused by missing dependencies?[/]"
    )

    console.print(f":thinking_face: {missing}")
