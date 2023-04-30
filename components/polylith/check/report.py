import ast
import itertools
from pathlib import Path
from typing import Any, Set

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


def is_internal_import(file_path: Path, import_name: str) -> bool:
    if "core_api_migration" in import_name:
        return True  # TODO: Remove this once core_api_migration is removed

    top_level_part = None
    if "components" in file_path.parts:
        top_level_part = file_path.parts.index("components")
    elif "bases" in file_path.parts:
        top_level_part = file_path.parts.index("bases")

    if top_level_part is None:
        return False

    component_name = file_path.parts[top_level_part + 2]
    import_component_name = import_name.split(".")[1]

    return component_name == import_component_name


def check_import(node: Any, file_path: Path) -> list[str]:
    if not isinstance(node, ast.Import):
        return []

    external_imports = []
    for imported_name in node.names:
        if (
            imported_name.name.startswith("oiq")
            and not imported_name.name.endswith(".interface")
            and not is_internal_import(file_path, imported_name.name)
        ):
            external_imports.append(
                f"Illegal import of {imported_name.name} at line {node.lineno} in file {file_path}."
            )
    return external_imports


def check_from_import(node: Any, file_path: Path) -> list[str]:
    if not isinstance(node, ast.ImportFrom) or not node.module:
        return []

    external_imports = []
    module = node.module
    if (
        module.startswith("oiq")
        and not (node.names[-1].name == "interface" or module.endswith(".interface"))
        and not is_internal_import(file_path, module)
    ):
        model_alias = node.names[-1].name
        external_imports.append(
            f"Illegal import of {module}.{model_alias} at line {node.lineno} in file {file_path}."
        )
    return external_imports


def check_function_calls(node: Any, file_path: Path) -> list[str]:
    if not isinstance(node, ast.Call):
        return []

    external_imports = []
    func = node.func
    if (
        isinstance(func, ast.Attribute)
        and func.attr == "get_model"
        and isinstance(func.value, ast.Name)
        and func.value.id == "apps"
    ):
        external_imports.append(
            f"Illegal call to apps.get_model(...) at line {node.lineno} in file {file_path}. Use a _get_<model-name>_model() function from an `interface` module instead."  # noqa: E501
        )
    return external_imports


def print_external_imports(root: Path, exclude_dirs: list[str] | None = None) -> bool:
    """Check for any imports of non-interface modules from external apps."""
    if exclude_dirs is None:
        exclude_dirs = [".venv"]
    console = Console(theme=theme.poly_theme)
    external_imports = []

    files = root.rglob("*.py")
    search_files = [
        file_path
        for file_path in files
        if not any(exclude_dir in file_path.parts for exclude_dir in exclude_dirs)
    ]

    external_imports = list(
        itertools.chain.from_iterable(
            itertools.chain.from_iterable(
                (
                    check_import(node, file_path),
                    check_from_import(node, file_path),
                    check_function_calls(node, file_path),
                )
                for file_path in search_files
                for node in ast.walk(ast.parse(file_path.read_text()))
            )
        )
    )
    if external_imports:
        console.print(
            "\n".join(external_imports)
            + "\n"
            + ":thinking_face: Found imports of internal modules from external apps. Use a function from an `interface` module instead."  # noqa: E501
        )
    return not external_imports


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
    has_no_external_models_imports = print_external_imports(root)

    return all([brick_result, libs_result, has_no_external_models_imports])


if __name__ == "__main__":
    import sys

    print_external_imports(Path(sys.argv[1]))
