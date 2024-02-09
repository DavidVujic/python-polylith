from pathlib import Path

from polylith import deps


def run(root: Path, ns: str, project_data: dict):
    brick_imports = deps.get_brick_imports(root, ns, project_data)

