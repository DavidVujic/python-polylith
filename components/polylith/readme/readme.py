from pathlib import Path

from polylith import repo

workspace_template = """\
# A Python Polylith repo

## Docs
The official Polylith documentation:
[high-level documentation](https://polylith.gitbook.io/polylith)

A Python implementation of the Polylith tool:
[python-polylith](https://github.com/DavidVujic/python-polylith)
"""

brick_template = """\
# {name} {brick}

{description}
"""


def create_readme(path: Path, template: str, **kwargs) -> None:
    fullpath = path / repo.readme_file

    if fullpath.exists():
        return

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(template.format(**kwargs))


def create_workspace_readme(path: Path, namespace: str) -> None:
    create_readme(path, workspace_template, namespace=namespace)


def create_brick_readme(path: Path, options: dict) -> None:
    brick = options["brick"]
    package = options["package"]
    description = options["description"]

    b = "component" if brick in repo.components_dir else "base"

    create_readme(
        path, brick_template, name=package, brick=b, description=description or ""
    )
