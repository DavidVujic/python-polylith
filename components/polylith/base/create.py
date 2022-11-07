from pathlib import Path

from polylith.repo import bases_dir
from polylith.block import create_block
from polylith.test import create_test


def create_base(path: Path, namespace: str, package: str) -> None:
    create_block(path, bases_dir, namespace, package)
    create_test(path, bases_dir, namespace, package)
