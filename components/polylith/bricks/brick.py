from pathlib import Path

from polylith.dirs import create_dir
from polylith.files import create_file
from polylith.interface import create_interface
from polylith.workspace import parser


def create_brick(
    root: Path, brick: str, namespace: str, package: str, modulename: str = "core"
) -> None:
    dirs_structure = parser.get_brick_structure_from_config(root)
    dirs = dirs_structure.format(brick=brick, namespace=namespace, package=package)
    d = create_dir(root, dirs)

    create_file(d, f"{modulename}.py")
    create_interface(d, namespace, package, modulename)
