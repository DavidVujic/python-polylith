from pathlib import Path
from typing import List

from polylith import check, workspace


def get_brick_imports(
    root: Path, ns: str, bases: List[str], components: List[str]
) -> dict:
    bases_paths = workspace.paths.collect_bases_paths(root, ns, set(bases))
    comp_paths = workspace.paths.collect_components_paths(root, ns, set(components))

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
