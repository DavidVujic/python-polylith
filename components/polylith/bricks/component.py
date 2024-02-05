from pathlib import Path
from typing import List

from polylith import configuration
from polylith.bricks.brick import create_brick
from polylith.repo import components_dir
from polylith.test import create_test


def create_component(path: Path, options: dict) -> None:
    extra = {"brick": components_dir}
    component_options = {**options, **extra}

    create_brick(path, component_options)
    create_test(path, component_options)


def is_brick_dir(p: Path) -> bool:
    return p.is_dir() and p.name not in {"__pycache__", ".venv", ".mypy_cache"}


def get_component_dirs(root: Path, top_dir, ns) -> list:
    theme = configuration.get_theme_from_config(root)
    dirs = top_dir if theme == "tdd" else f"{top_dir}/{ns}"

    component_dir = root / dirs

    if not component_dir.exists():
        return []

    return [f for f in component_dir.iterdir() if is_brick_dir(f)]


def get_components_data(
    root: Path, ns: str, top_dir: str = components_dir
) -> List[dict]:
    dirs = get_component_dirs(root, top_dir, ns)

    return [{"name": d.name} for d in dirs]
