from pathlib import Path

from polylith import check, info, workspace


def get_brick_imports(root: Path, ns: str, project_data: dict) -> dict:
    bases = {b for b in project_data.get("bases", [])}
    components = {c for c in project_data.get("components", [])}

    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    components_paths = workspace.paths.collect_components_paths(root, ns, components)

    brick_imports_in_bases = check.collect.extract_bricks(bases_paths, ns)
    brick_imports_in_components = check.collect.extract_bricks(components_paths, ns)

    return {
        "bases": check.collect.with_unknown_components(
            root, ns, brick_imports_in_bases
        ),
        "components": check.collect.with_unknown_components(
            root, ns, brick_imports_in_components
        ),
    }


def calculate_diff(
    root: Path,
    namespace: str,
    project_data: dict,
    workspace_data: dict,
) -> dict:
    brick_imports = get_brick_imports(root, namespace, project_data)

    all_bases = workspace_data["bases"]
    all_components = workspace_data["components"]

    bases = project_data["bases"]
    components = project_data["components"]

    is_project = info.is_project(project_data)

    if is_project:
        brick_diff = check.collect.imports_diff(brick_imports, bases, components)
    else:
        all_bricks = set().union(all_bases, all_components)
        brick_diff = check.collect.diff(all_bricks, bases, components)

    bases_diff = {b for b in brick_diff if b in all_bases}
    components_diff = {b for b in brick_diff if b in all_components}

    return {
        "name": project_data["name"],
        "path": project_data["path"],
        "is_project": is_project,
        "bases": bases_diff,
        "components": components_diff,
        "brick_imports": brick_imports,
    }
