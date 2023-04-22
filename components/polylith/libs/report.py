import difflib
from pathlib import Path
from typing import Set

from polylith import info, workspace
from polylith.libs import grouping
from polylith.reporting import theme
from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.table import Table


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


def flatten_brick_imports(brick_imports: dict) -> Set[str]:
    bases_imports = flatten_imports(brick_imports, "bases")
    components_imports = flatten_imports(brick_imports, "components")

    return set().union(bases_imports, components_imports)


def filter_close_matches(unknown_imports: Set[str], deps: Set[str]) -> Set[str]:
    return {u for u in unknown_imports if not difflib.get_close_matches(u, deps)}


def calculate_diff(brick_imports: dict, deps: Set[str]) -> Set[str]:
    imports = flatten_brick_imports(brick_imports)
    unknown_imports = imports.difference(deps)

    return filter_close_matches(unknown_imports, deps)


def print_libs_summary(brick_imports: dict, project_data: dict) -> None:
    console = Console(theme=theme.poly_theme)

    name = project_data["name"]
    is_project = info.is_project(project_data)

    printable_name = f"[proj]{name}[/]" if is_project else "[data]development[/]"
    console.print(
        Padding(f"[data]Libraries summary for [/]{printable_name}", (1, 0, 1, 0))
    )

    bases_imports = flatten_imports(brick_imports, "bases")
    components_imports = flatten_imports(brick_imports, "components")

    console.print(f"[base]Libraries used in bases[/]: [data]{len(bases_imports)}[/]")
    console.print(
        f"[comp]libraries used in components[/]: [data]{len(components_imports)}[/]"
    )


def print_libs_in_bricks(brick_imports: dict) -> None:
    bases_imports = flatten_imports(brick_imports, "bases")
    components_imports = flatten_imports(brick_imports, "components")

    if not bases_imports and not components_imports:
        return

    console = Console(theme=theme.poly_theme)
    table = Table(box=box.SIMPLE_HEAD)

    bases = brick_imports.get("bases", {})
    components = brick_imports.get("components", {})

    table.add_column("[data]brick[/]")
    table.add_column("[data]libraries[/]")

    for brick, imports in bases.items():
        table.add_row(f"[base]{brick}[/]", ", ".join(sorted(imports)))

    for brick, imports in components.items():
        table.add_row(f"[comp]{brick}[/]", ", ".join(sorted(imports)))

    console.print(table, overflow="ellipsis")


def print_missing_installed_libs(
    brick_imports: dict, third_party_libs: Set[str], project_name: str
) -> bool:
    diff = calculate_diff(brick_imports, third_party_libs)

    if not diff:
        return True

    console = Console(theme=theme.poly_theme)

    missing = ", ".join(sorted(diff))

    console.print(
        f"[data]Could not locate all libraries in [/][proj]{project_name}[/]. [data]Caused by missing dependencies?[/]"
    )

    console.print(f":thinking_face: {missing}")
    return False
