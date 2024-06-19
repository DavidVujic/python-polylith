from pathlib import Path
from typing import Set

from polylith import check, distributions


def collect_known_aliases(project_data: dict, options: dict) -> Set[str]:
    deps = project_data["deps"]
    library_alias = options["alias"]

    return distributions.known_aliases_and_sub_dependencies(deps, library_alias)


def run(root: Path, ns: str, project_data: dict, options: dict) -> bool:
    is_verbose = options["verbose"]
    is_quiet = options["quiet"]
    is_strict = options["strict"]

    name = project_data["name"]

    collected_imports = check.report.collect_all_imports(root, ns, project_data)
    collected_libs = collect_known_aliases(project_data, options)

    details = check.report.create_report(
        project_data,
        collected_imports,
        collected_libs,
        is_strict,
    )

    res = all([not details["brick_diff"], not details["libs_diff"]])

    if not is_quiet:
        check.report.print_missing_deps(details["brick_diff"], name)
        check.report.print_missing_deps(details["libs_diff"], name)

        if is_verbose:
            check.report.print_brick_imports(details["brick_imports"])
            check.report.print_brick_imports(details["third_party_imports"])

    return res
