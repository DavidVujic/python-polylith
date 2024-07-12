from functools import reduce
from pathlib import Path
from typing import List, Set

from polylith import distributions
from polylith.libs import report


def missing_libs(project_data: dict, imports: dict, options: dict) -> bool:
    is_strict = options["strict"]
    library_alias = options["alias"]

    name = project_data["name"]
    deps = project_data["deps"]

    brick_imports = imports[name]

    libs = distributions.known_aliases_and_sub_dependencies(
        deps, library_alias, options
    )

    return report.print_missing_installed_libs(
        brick_imports,
        libs,
        name,
        is_strict,
    )


def flatten_imports(acc: dict, item: dict) -> dict:
    bases = item.get("bases", {})
    components = item.get("components", {})

    return {
        "bases": {**acc.get("bases", {}), **bases},
        "components": {**acc.get("components", {}), **components},
    }


def run_library_versions(
    projects_data: List[dict], all_projects_data: List[dict], options: dict
) -> None:
    development_data = next(p for p in all_projects_data if p["type"] == "development")
    filtered_projects_data = [p for p in projects_data if p["type"] != "development"]

    report.print_libs_in_projects(development_data, filtered_projects_data, options)


def run(
    root: Path,
    ns: str,
    projects_data: List[dict],
    options: dict,
) -> Set[bool]:
    imports = {
        p["name"]: report.get_third_party_imports(root, ns, p) for p in projects_data
    }

    flattened: dict = reduce(flatten_imports, imports.values(), {})

    report.print_libs_summary()
    report.print_libs_in_bricks(flattened)

    return {missing_libs(p, imports, options) for p in projects_data}
