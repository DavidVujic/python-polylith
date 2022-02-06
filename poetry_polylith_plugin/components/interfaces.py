from pathlib import Path

from poetry_polylith_plugin.components.files import create_file

template = """\
from {namespace}.{package} import {modulename}

__all__ = ["{modulename}"]
"""


def create_interface(path: Path, namespace: str, package: str, modulename: str):
    interface = create_file(path, "__init__.py")

    content = template.format(
        namespace=namespace, package=package, modulename=modulename
    )

    interface.write_text(content, newline="\n")
