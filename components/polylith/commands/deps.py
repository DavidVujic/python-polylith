from pathlib import Path

from polylith import deps


def run(root: Path, ns: str, project_data: dict):
    res = deps.get_brick_imports(root, ns, project_data)

    flattened = {**res["bases"], **res["components"]}

    deps.print_deps(project_data, flattened)
