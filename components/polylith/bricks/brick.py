from pathlib import Path
from typing import Union

from polylith.dirs import create_dir
from polylith.files import create_file
from polylith.interface import create_interface
from polylith.readme import create_brick_readme
from polylith.workspace import parser


def create_brick(
    root: Path,
    brick: str,
    namespace: str,
    package: str,
    description: Union[str, None],
    modulename: str = "core",
) -> None:
    dirs_structure = parser.get_brick_structure_from_config(root)
    dirs = dirs_structure.format(brick=brick, namespace=namespace, package=package)
    d = create_dir(root, dirs)

    create_file(d, f"{modulename}.py")
    create_interface(d, namespace, package, modulename, description)

    if parser.is_readme_generation_enabled(root):
        create_brick_readme(d, package, brick, description)
