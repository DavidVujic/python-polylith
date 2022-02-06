from pathlib import Path

from poetry_polylith_plugin.components.dirs import create_dir
from poetry_polylith_plugin.components.files import create_file
from poetry_polylith_plugin.components.interfaces import create_interface


def create_block(
    path: Path, name: str, namespace: str, package: str, modulename: str = "core"
):
    d = create_dir(path, f"{name}/{package}/src/{namespace}/{package}")

    create_file(d, f"{modulename}.py")
    create_interface(d, namespace, package, modulename)
