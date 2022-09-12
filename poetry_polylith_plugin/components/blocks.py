from pathlib import Path

from poetry_polylith_plugin.components.dirs import create_dir
from poetry_polylith_plugin.components.files import create_file
from poetry_polylith_plugin.components.interfaces import create_interface
from poetry_polylith_plugin.components.toml import create_empty_toml


def create_block(
    path: Path, name: str, namespace: str, package: str, modulename: str = "core"
):
    block_path = create_dir(path, f"{name}/{package}")
    create_empty_toml(package, block_path)

    src_path = create_dir(block_path, f"src/{namespace}/{package}")
    create_file(src_path, f"{modulename}.py")
    create_interface(src_path, namespace, package, modulename)
