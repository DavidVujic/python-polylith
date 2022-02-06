from pathlib import Path

from poetry_polylith_plugin.components.blocks import create_block

dir_name = "components"


def create_component(path: Path, namespace: str, package: str):
    create_block(path, dir_name, namespace, package)
