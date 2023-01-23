from pathlib import Path

from polylith.files import create_file

template = """\
from {namespace}.{package} import {modulename}

__all__ = ["{modulename}"]
"""


def to_namespaced_path(package: str) -> str:
    parts = package.split("/")

    return ".".join(parts)


def create_interface(path: Path, namespace: str, package: str, modulename: str) -> None:
    interface = create_file(path, "__init__.py")

    package_path = to_namespaced_path(package)

    content = template.format(
        namespace=namespace, package=package_path, modulename=modulename
    )

    interface.write_text(content)
