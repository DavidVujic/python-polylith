from pathlib import Path

from polylith.bricks.brick import create_brick
from polylith.repo import components_dir
from polylith.test import create_test
from polylith import workspace


def create_component(path: Path, namespace: str, package: str) -> None:
    create_brick(path, components_dir, namespace, package)
    create_test(path, components_dir, namespace, package)


def get_component_dirs(root: Path, top_dir, ns) -> list:
    theme = workspace.parser.get_theme_from_config(root)
    dirs = top_dir if theme == "tdd" else f"{top_dir}/{ns}"

    component_dir = root / dirs

    if not component_dir.exists():
        return []

    return [f for f in component_dir.iterdir() if f.is_dir()]


def get_components_data(
    root: Path, ns: str, top_dir: str = components_dir
) -> list[dict]:
    dirs = get_component_dirs(root, top_dir, ns)

    return [{"name": d.name} for d in dirs]
