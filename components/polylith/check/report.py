from pathlib import Path
from typing import Set

from polylith import imports, libs, workspace
from polylith.check import collect, grouping
from polylith.reporting import theme
from rich.console import Console


def _print_imports(bricks: dict, brick_type: str) -> None:
    console = Console(theme=theme.poly_theme)

    items = sorted(bricks.items())
    tag = "base" if brick_type == "bases" else "comp"

    for item in items:
        key, values = item

        imports_in_brick = values.difference({key})

        if not imports_in_brick:
            continue

        joined = ", ".join(sorted(imports_in_brick))
        message = f":information: [{tag}]{key}[/] is importing [data]{joined}[/]"
        console.print(message)


def print_brick_imports(brick_imports: dict) -> None:
    bases = brick_imports["bases"]
    components = brick_imports["components"]

    _print_imports(bases, "bases")
    _print_imports(components, "components")


def print_missing_deps(diff: Set[str], project_name: str) -> None:
    if not diff:
        return

    console = Console(theme=theme.poly_theme)

    missing = ", ".join(sorted(diff))

    console.print(f":thinking_face: Cannot locate {missing} in {project_name}")


def collect_all_imports(root: Path, ns: str, project_data: dict) -> dict:
    bases = {b for b in project_data.get("bases", [])}
    components = {c for c in project_data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    all_imports_in_bases = imports.fetch_all_imports(bases_paths)
    all_imports_in_components = imports.fetch_all_imports(components_paths)

    brick_imports = {
        "bases": grouping.extract_brick_imports(all_imports_in_bases, ns),
        "components": grouping.extract_brick_imports(all_imports_in_components, ns),
    }

    third_party_imports = {
        "bases": libs.extract_third_party_imports(all_imports_in_bases, ns),
        "components": libs.extract_third_party_imports(all_imports_in_components, ns),
    }

    return {"brick_imports": brick_imports, "third_party_imports": third_party_imports}


def create_report(
    project_data: dict,
    collected_imports: dict,
    third_party_libs: Set,
    is_strict: bool = False,
) -> dict:
    bases = {b for b in project_data.get("bases", [])}
    components = {c for c in project_data.get("components", [])}

    brick_imports = collected_imports["brick_imports"]
    third_party_imports = collected_imports["third_party_imports"]

    brick_diff = collect.imports_diff(brick_imports, bases, components)
    libs_diff = libs.report.calculate_diff(
        third_party_imports, third_party_libs, is_strict
    )

    return {
        "brick_imports": brick_imports,
        "third_party_imports": third_party_imports,
        "brick_diff": brick_diff,
        "libs_diff": libs_diff,
    }
