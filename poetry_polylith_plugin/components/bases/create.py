from pathlib import Path

from poetry_polylith_plugin.components.bases.constants import dir_name
from poetry_polylith_plugin.components.blocks import create_block
from poetry_polylith_plugin.components.tests import create_test


def create_base(path: Path, namespace: str, package: str):
    create_block(path, dir_name, namespace, package)
    create_test(path, dir_name, namespace, package)
