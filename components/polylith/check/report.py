from pathlib import Path
from typing import Set, Tuple

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

        if imports_in_brick:
            console.print(
                f":information: [data]{key}[/] is importing [data]{', '.join(imports_in_brick)}[/]"
            )


def print_missing_deps(diff: Set[str], project_name: str) -> bool:
    if not diff:
        return True

    console = Console(theme=theme.poly_theme)

    missing = ", ".join(sorted(diff))

    console.print(f":thinking_face: Cannot locate {missing} in {project_name}")
    return False


def fetch_brick_imports(root: Path, ns: str, all_imports: dict) -> dict:
    extracted = grouping.extract_brick_imports(all_imports, ns)

    return collect.with_unknown_components(root, ns, extracted)


def print_report(
    root: Path,
    ns: str,
    project_data: dict,
    third_party_libs: Set,
) -> Tuple[bool, dict, dict]:
    name = project_data["name"]

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

    brick_diff = collect.imports_diff(brick_imports, list(bases), list(components))
    brick_result = print_missing_deps(brick_diff, name)

    libs_diff = libs.report.calculate_diff(third_party_imports, third_party_libs)
    libs_result = print_missing_deps(libs_diff, name)

    return all([brick_result, libs_result]), brick_imports, third_party_imports
