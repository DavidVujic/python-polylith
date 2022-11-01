from pathlib import Path

from polylith.block import create_block
from polylith.component.constants import dir_name
from polylith.test import create_test


def create_component(path: Path, namespace: str, package: str) -> None:
    create_block(path, dir_name, namespace, package)
    create_test(path, dir_name, namespace, package)
