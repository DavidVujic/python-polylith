import importlib.metadata
from pathlib import Path

from polylith import alias, check, distributions


def run(root: Path, ns: str, project_data: dict, options: dict) -> bool:
    is_verbose = options["verbose"]
    is_quiet = options["quiet"]
    is_strict = options["strict"]
    library_alias = options["alias"]

    third_party_libs = project_data["deps"]
    name = project_data["name"]

    collected_imports = check.report.collect_all_imports(root, ns, project_data)
    dists = importlib.metadata.distributions()

    known_aliases = distributions.distributions_packages(dists)
    known_aliases.update(alias.parse(library_alias))

    extra = alias.pick(known_aliases, third_party_libs)

    libs = third_party_libs.union(extra)

    details = check.report.create_report(
        project_data,
        collected_imports,
        libs,
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
