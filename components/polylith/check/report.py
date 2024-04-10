from pathlib import Path
from typing import Set

from polylith import imports, libs, workspace
from polylith.check import collect, grouping
from polylith.reporting import theme
from rich.console import Console


def print_brick_imports(brick_imports: dict) -> None:
    console = Console(theme=theme.poly_theme)

    bases = brick_imports["bases"]
    components = brick_imports["components"]

    bricks = {**bases, **components}

    for key, values in bricks.items():
        imports_in_brick = values.difference({key})

        if not imports_in_brick:
            continue

        joined = ", ".join(imports_in_brick)
        message = f":information: [data]{key}[/] is importing [data]{joined}[/]"
        console.print(message)


def print_missing_deps(diff: Set[str], project_name: str) -> None:
    if not diff:
        return

    console = Console(theme=theme.poly_theme)

    missing = ", ".join(sorted(diff))

    console.print(f":thinking_face: Cannot locate {missing} in {project_name}")


def fetch_brick_imports(root: Path, ns: str, all_imports: dict) -> dict:
    extracted = grouping.extract_brick_imports(all_imports, ns)

    return collect.with_unknown_components(root, ns, extracted)


def collect_all_imports(root: Path, ns: str, project_data: dict) -> dict:
    bases = {b for b in project_data.get("bases", [])}
    components = {c for c in project_data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    all_imports_in_bases = imports.fetch_all_imports(bases_paths)
    all_imports_in_components = imports.fetch_all_imports(components_paths)

    brick_imports = {
        "bases": fetch_brick_imports(root, ns, all_imports_in_bases),
        "components": fetch_brick_imports(root, ns, all_imports_in_components),
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
