from functools import reduce
from pathlib import Path
from typing import List, Tuple

from polylith import check, distributions, libs


def extract_libs_from_project_lock_file(project_data: dict) -> dict:
    lock_file_data = libs.pick_lock_file(project_data["path"])

    if not lock_file_data:
        return {}

    filename = lock_file_data["filename"]
    filetype = lock_file_data["filetype"]

    third_party_libs = libs.extract_libs(project_data, filename, filetype)

    return {"deps": {"items": third_party_libs, "source": filename}}


def extract_libs_from_workspace_lock_file(root: Path, project_data: dict) -> dict:
    lock_file_data = libs.pick_lock_file(root)

    if not lock_file_data:
        return {}

    filename = lock_file_data["filename"]
    filetype = lock_file_data["filetype"]

    data = libs.get_workspace_enabled_lock_file_data(root, filename, filetype)

    if not data:
        return {}

    third_party_libs = libs.extract_workspace_member_libs(data, project_data)

    return {"deps": {"items": third_party_libs, "source": filename}}


def extract_libs_from_lock_file(root: Path, project_data: dict) -> dict:
    from_project = extract_libs_from_project_lock_file(project_data)

    return from_project or extract_libs_from_workspace_lock_file(root, project_data)


def with_third_party_libs_from_lock_file(root: Path, project_data: dict) -> dict:
    third_party_libs = extract_libs_from_lock_file(root, project_data)

    return {**project_data, **third_party_libs}


def check_libs_versions(
    projects_data: List[dict], all_projects_data: List[dict], options: dict
) -> bool:
    is_strict = options["strict"]
    is_quiet = options["quiet"]

    if not is_strict:
        return True

    development_data = next(p for p in all_projects_data if p["type"] == "development")

    libraries = libs.report.libs_with_different_versions(
        development_data, projects_data
    )

    if not is_quiet:
        libs.report.print_libs_with_different_versions(
            libraries, development_data, projects_data, options
        )

    return False if libraries else True


def run_each(
    root: Path, ns: str, project_data: dict, options: dict
) -> Tuple[bool, dict]:
    is_quiet = options["quiet"]
    is_strict = options["strict"]

    name = project_data["name"]
    deps = project_data["deps"]
    alias = options["alias"]

    from_lock_file = libs.is_from_lock_file(deps)

    collected_imports = check.report.collect_all_imports(root, ns, project_data)
    collected_libs = distributions.known_aliases_and_sub_dependencies(
        deps,
        alias,
        options,
        from_lock_file,
    )

    details = check.report.create_report(
        project_data,
        collected_imports,
        collected_libs,
        is_strict or from_lock_file,
    )

    res = all([not details["brick_diff"], not details["libs_diff"]])

    if not is_quiet:
        check.report.print_missing_deps(details["brick_diff"], name)
        check.report.print_missing_deps(details["libs_diff"], name)

    return res, details


def _merge(data: List[dict], key: str) -> dict:
    return reduce(lambda acc, d: {**acc, **d[key]}, data, {})


def _print_brick_imports(all_imports: List[dict]) -> None:
    merged_bases = _merge(all_imports, "bases")
    merged_components = _merge(all_imports, "components")

    merged = {"bases": merged_bases, "components": merged_components}

    check.report.print_brick_imports(merged)


def run(root: Path, ns: str, projects_data: List[dict], options: dict) -> bool:
    is_verbose = options["verbose"] and not options["quiet"]
    res = [run_each(root, ns, p, options) for p in projects_data]
    results = [r[0] for r in res]

    if is_verbose:
        brick_imports = [r[1]["brick_imports"] for r in res]
        third_party_imports = [r[1]["third_party_imports"] for r in res]

        _print_brick_imports(brick_imports)
        _print_brick_imports(third_party_imports)

    return all(results)
