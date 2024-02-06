from pathlib import Path

from polylith import check, workspace


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
