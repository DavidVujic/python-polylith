from pathlib import Path
from typing import List

from polylith import distributions, repo, toml
from polylith.libs import report


def run(root: Path, ns: str, project_data: dict, options: dict) -> bool:
    is_strict = options["strict"]
    library_alias = options["alias"]

    name = project_data["name"]
    deps = project_data["deps"]

    brick_imports = report.get_third_party_imports(root, ns, project_data)

    report.print_libs_summary(brick_imports, project_data)
    report.print_libs_in_bricks(brick_imports)

    libs = distributions.known_aliases_and_sub_dependencies(deps, library_alias)

    return report.print_missing_installed_libs(
        brick_imports,
        libs,
        name,
        is_strict,
    )


def compare_versions(all_projects_data: List[dict], projects_data: List[dict]) -> None:
    development_data = next(p for p in all_projects_data if p["type"] == "development")

    dev_toml = toml.read_toml_document(development_data["path"] / repo.default_toml)
    res = toml.parse_project_dependencies(dev_toml)

    print(res)
