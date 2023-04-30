from pathlib import Path

from polylith.files import create_file
from polylith.workspace import parser

template = """\
# Polylith Bricks
from {namespace}.{package} import {modulename}


def test_sample():
    assert {modulename} is not None
"""


def create_test(
    root: Path, brick: str, namespace: str, package: str, modulename: str = "interface"
) -> None:
    if not parser.is_test_generation_enabled(root):
        return

    path_kwargs = {"brick": brick, "namespace": namespace, "package": package}

    brick_structure = parser.get_brick_structure_from_config(root)
    brick_path = brick_structure.format(**path_kwargs)

    d = root / brick_path

    test_file = create_file(d, f"test_{modulename}.py")

    content = template.format(
        namespace=namespace, package=package, modulename=modulename
    )

    test_file.write_text(content)
