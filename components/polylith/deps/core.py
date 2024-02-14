from pathlib import Path
from typing import Set

from polylith import check, workspace


def get_brick_imports(
    root: Path, ns: str, bases: Set[str], components: Set[str]
) -> dict:
    bases_paths = workspace.paths.collect_bases_paths(root, ns, bases)
    comp_paths = workspace.paths.collect_components_paths(root, ns, components)

    brick_imports_in_bases = check.collect.extract_bricks(bases_paths, ns)
    brick_imports_in_components = check.collect.extract_bricks(comp_paths, ns)

    return {
        "bases": check.collect.with_unknown_components(
            root, ns, brick_imports_in_bases
        ),
        "components": check.collect.with_unknown_components(
            root, ns, brick_imports_in_components
        ),
    }
