from pathlib import Path

from polylith import check, deps, info


def calculate_diff(
    root: Path,
    namespace: str,
    project_data: dict,
    workspace_data: dict,
) -> dict:
    bases = set(project_data["bases"])
    components = set(project_data["components"])

    all_bases = workspace_data["bases"]
    all_components = workspace_data["components"]

    brick_imports = deps.get_brick_imports(root, namespace, bases, components)
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
