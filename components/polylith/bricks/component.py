from pathlib import Path

from polylith.bricks.brick import create_brick
from polylith.repo import components_dir
from polylith.test import create_test


def create_component(path: Path, options: dict) -> None:
    extra = {"brick": components_dir}
    component_options = {**options, **extra}

    create_brick(path, component_options)
    create_test(path, component_options)
