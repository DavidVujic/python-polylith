from pathlib import Path
from typing import Union

from polylith.files import create_file

template_docstring = """\
\"\"\"
{description}
\"\"\"

"""

template_content = """\
from {namespace}.{package} import {modulename}

__all__ = ["{modulename}"]

"""


def to_namespaced_path(package: str) -> str:
    parts = package.split("/")

    return ".".join(parts)


def create_interface(
    path: Path,
    namespace: str,
    package: str,
    modulename: str,
    description: Union[str, None],
) -> None:
    interface = create_file(path, "__init__.py")

    package_path = to_namespaced_path(package)

    docstring = (
        template_docstring.format(description=description) if description else ""
    )

    content = template_content.format(
        namespace=namespace, package=package_path, modulename=modulename
    )

    interface.write_text(docstring + content)
