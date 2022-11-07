from pathlib import Path

from polylith.block import create_block
from polylith.repo import components_dir
from polylith.test import create_test


def create_component(path: Path, namespace: str, package: str) -> None:
    create_block(path, components_dir, namespace, package)
    create_test(path, components_dir, namespace, package)
