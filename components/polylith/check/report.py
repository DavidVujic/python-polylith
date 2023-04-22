from pathlib import Path
from typing import Set

from polylith import imports, libs, workspace
from polylith.check import grouping
from polylith.reporting import theme
from rich.console import Console


def print_missing_deps(brick_imports: dict, deps: Set[str], project_name: str) -> bool:
    diff = libs.report.calculate_diff(brick_imports, deps)

    if not diff:
        return True

    console = Console(theme=theme.poly_theme)

    missing = ", ".join(sorted(diff))

    console.print(f":thinking_face: Cannot locate {missing} in {project_name}")
    return False


def print_report(
    root: Path, ns: str, project_data: dict, third_party_libs: Set
) -> bool:
    name = project_data["name"]

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

    packages = set().union(bases, components)

    brick_result = print_missing_deps(brick_imports, packages, name)
    libs_result = print_missing_deps(third_party_imports, third_party_libs, name)

    return all([brick_result, libs_result])
