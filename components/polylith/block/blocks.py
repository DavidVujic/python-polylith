from pathlib import Path

from polylith.dirs import create_dir
from polylith.files import create_file
from polylith.interface import create_interface


def create_block(
    path: Path, name: str, namespace: str, package: str, modulename: str = "core"
) -> None:
    d = create_dir(path, f"{name}/{namespace}/{package}")

    create_file(d, f"{modulename}.py")
    create_interface(d, namespace, package, modulename)
