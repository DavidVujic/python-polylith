from pathlib import Path

from polylith.bricks import brick, component
from polylith.repo import bases_dir
from polylith.test import create_test


def create_base(path: Path, namespace: str, package: str) -> None:
    brick.create_brick(path, bases_dir, namespace, package)
    create_test(path, bases_dir, namespace, package)


def get_bases_data(path: Path, ns: str) -> list[dict]:
    return component.get_components_data(path, ns, bases_dir)
