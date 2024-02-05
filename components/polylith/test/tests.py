from pathlib import Path

from polylith.dirs import create_dir
from polylith.files import create_file
from polylith import configuration

template = """\
from {namespace}.{package} import {modulename}


def test_sample():
    assert {modulename} is not None
"""


def create_test(root: Path, options: dict) -> None:
    if not configuration.is_test_generation_enabled(root):
        return

    brick = options["brick"]
    namespace = options["namespace"]
    package = options["package"]
    modulename = options["modulename"]

    dirs_structure = configuration.get_tests_structure_from_config(root)
    dirs = dirs_structure.format(brick=brick, namespace=namespace, package=package)
    d = create_dir(root, dirs)

    create_file(d, "__init__.py")
    test_file = create_file(d, f"test_{modulename}.py")

    content = template.format(
        namespace=namespace, package=package, modulename=modulename
    )

    test_file.write_text(content)
