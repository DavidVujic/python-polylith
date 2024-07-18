import difflib
from operator import itemgetter
from pathlib import Path
from typing import List, Set, Union

from polylith import workspace
from polylith.libs import grouping
from polylith.reporting import theme
from rich import box, markup
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


def filter_close_matches(
    unknown_imports: Set[str], dependencies: Set[str], cutoff: float
) -> Set[str]:
    unknowns = {str.lower(u) for u in unknown_imports}
    deps = {str.lower(d).replace("-", "_") for d in dependencies}

    return {
        u for u in unknowns if not difflib.get_close_matches(u, deps, cutoff=cutoff)
    }


def get_unknowns(brick_imports: dict, deps: Set[str]) -> Set[str]:
    imports = flatten_brick_imports(brick_imports)

    return imports.difference(deps)


def calculate_diff(
    brick_imports: dict, deps: Set[str], is_strict: bool = False
) -> Set[str]:
    unknown_imports = get_unknowns(brick_imports, deps)

    cutoff = 0.6 if not is_strict else 1

    return filter_close_matches(unknown_imports, deps, cutoff)


def print_libs_summary() -> None:
    console = Console(theme=theme.poly_theme)

    console.print(Padding("[data]Libraries in bricks[/]", (1, 0, 0, 0)))


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
    table.add_column("[data]library[/]")

    for brick, imports in sorted(components.items(), key=itemgetter(0)):
        table.add_row(f"[comp]{brick}[/]", ", ".join(sorted(imports)))

    for brick, imports in sorted(bases.items(), key=itemgetter(0)):
        table.add_row(f"[base]{brick}[/]", ", ".join(sorted(imports)))

    console.print(table, overflow="ellipsis")


def print_missing_installed_libs(
    brick_imports: dict,
    third_party_libs: Set[str],
    project_name: str,
    is_strict: bool = False,
) -> bool:
    diff = calculate_diff(brick_imports, third_party_libs, is_strict)

    if not diff:
        return True

    console = Console(theme=theme.poly_theme)

    missing = ", ".join(sorted(diff))

    console.print(
        f"[data]Could not locate all libraries in [/][proj]{project_name}[/]. [data]Caused by missing dependencies?[/]"
    )

    console.print(f":thinking_face: {missing}")
    return False


def printable_version(version: Union[str, None], is_same_version: bool) -> str:
    ver = version or "-"
    markup = "data" if is_same_version else "bold"

    return f"[{markup}]{ver}[/]"


def get_version(lib: str, project_data: dict) -> str:
    return project_data["deps"]["items"].get(lib)


def find_version(
    lib: str, project_name: str, projects_data: List[dict]
) -> Union[str, None]:
    project_data = next(p for p in projects_data if p["name"] == project_name)

    return get_version(lib, project_data)


def printable_header(header: str, short: bool) -> str:
    return "\n".join(header) if short else header


def is_same_version(versions: list) -> bool:
    unique = set([v for v in versions if v])

    return len(unique) == 1 if unique else True


def libs_in_projects_table(
    development_data: dict,
    projects_data: List[dict],
    libraries: set,
    options: dict,
) -> Table:
    table = Table(box=box.SIMPLE_HEAD)

    short = options["short"]

    project_names = sorted({p["name"] for p in projects_data})
    project_headers = [f"[proj]{printable_header(n, short)}[/]" for n in project_names]
    dev_header = printable_header("development", short)
    headers = ["[data]library[/]"] + project_headers + [f"[data]{dev_header}[/]"]

    for header in headers:
        table.add_column(header)

    for lib in sorted(libraries):
        proj_versions = [find_version(lib, n, projects_data) for n in project_names]
        dev_version = get_version(lib, development_data)

        is_same = is_same_version(proj_versions + [dev_version])
        printable_proj_versions = [printable_version(v, is_same) for v in proj_versions]
        printable_dev_version = printable_version(dev_version, is_same)

        cols = [markup.escape(lib)] + printable_proj_versions + [printable_dev_version]

        table.add_row(*cols)

    return table


def flattened_lib_names(projects_data: List[dict]) -> Set[str]:
    return {k for proj in projects_data for k, _v in proj["deps"]["items"].items()}


def print_libs_in_projects(
    development_data: dict, projects_data: List[dict], options: dict
) -> None:
    flattened = flattened_lib_names(projects_data)

    if not flattened:
        return

    table = libs_in_projects_table(development_data, projects_data, flattened, options)

    console = Console(theme=theme.poly_theme)

    console.print(Padding("[data]Library versions in projects[/]", (1, 0, 0, 0)))
    console.print(table, overflow="ellipsis")


def has_different_version(
    lib: str, development_data: dict, projects_data: List[dict]
) -> bool:
    proj_versions = [get_version(lib, p) for p in projects_data]
    dev_version = get_version(lib, development_data)

    return not is_same_version(proj_versions + [dev_version])


def libs_with_different_versions(
    development_data: dict, projects_data: List[dict]
) -> Set[str]:
    flattened = flattened_lib_names(projects_data)
    return {
        f
        for f in flattened
        if has_different_version(f, development_data, projects_data)
    }


def print_libs_with_different_versions(
    libraries: Set[str],
    development_data: dict,
    projects_data: List[dict],
    options: dict,
) -> None:
    if not libraries:
        return

    table = libs_in_projects_table(development_data, projects_data, libraries, options)

    console = Console(theme=theme.poly_theme)
    console.print(
        Padding("[data]Different library versions in projects[/]", (1, 0, 0, 0))
    )
    console.print(table, overflow="ellipsis")
