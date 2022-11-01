from pathlib import Path

from polylith.dirs import create_dir
from polylith.files import create_file

template = """\
from {namespace}.{package} import {modulename}


def test_sample():
    assert {modulename} is not None
"""


def create_test(
    path: Path, name: str, namespace: str, package: str, modulename: str = "core"
) -> None:
    d = create_dir(path, f"{name}/test_{namespace}/{package}")

    create_file(d, "__init__.py")
    test_file = create_file(d, f"test_{modulename}.py")

    content = template.format(
        namespace=namespace, package=package, modulename=modulename
    )

    test_file.write_text(content, newline="\n")
