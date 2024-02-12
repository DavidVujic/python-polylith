from pathlib import Path
from typing import List

from polylith import deps


def run(root: Path, ns: str, bases: List[str], components: List[str]):
    brick_imports = deps.get_brick_imports(root, ns, bases, components)

    flattened = {**brick_imports["bases"], **brick_imports["components"]}

    deps.print_deps(bases, components, flattened)
