from pathlib import Path

from polylith.bricks.brick import create_brick
from polylith.repo import components_dir
from polylith.test import create_test


def create_component(path: Path, namespace: str, package: str) -> None:
    create_brick(path, components_dir, namespace, package)
    create_test(path, components_dir, namespace, package)


def get_component_dirs(path: Path, top_dir, ns) -> list:
    component_dir = path / top_dir / ns

    if not component_dir.exists():
        return []

    return [f for f in component_dir.iterdir() if f.is_dir()]


def get_components_data(
    path: Path, ns: str, top_dir: str = components_dir
) -> list[dict]:
    dirs = get_component_dirs(path, top_dir, ns)

    return [{"name": d.name} for d in dirs]
