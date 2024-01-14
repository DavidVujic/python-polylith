from pathlib import Path

from polylith import alias
from polylith.libs import report


def run(root: Path, ns: str, project_data: dict, options: dict) -> bool:
    is_strict = options["strict"]
    library_alias = options["alias"]

    name = project_data["name"]
    third_party_libs = project_data["deps"]

    brick_imports = report.get_third_party_imports(root, ns, project_data)

    report.print_libs_summary(brick_imports, project_data)
    report.print_libs_in_bricks(brick_imports)

    library_aliases = alias.parse(library_alias)
    extra = alias.pick(library_aliases, third_party_libs)

    libs = third_party_libs.union(extra)

    return report.print_missing_installed_libs(
        brick_imports,
        libs,
        name,
        is_strict,
    )
