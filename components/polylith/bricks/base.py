from pathlib import Path
from typing import List, Union

from polylith.bricks import component
from polylith.bricks.brick import create_brick
from polylith.repo import bases_dir
from polylith.test import create_test


def create_base(path: Path, namespace: str, package: str, description: Union[str, None]) -> None:
    create_brick(path, bases_dir, namespace, package, description)
    create_test(path, bases_dir, namespace, package)


def get_bases_data(path: Path, ns: str) -> List[dict]:
    return component.get_components_data(path, ns, bases_dir)
