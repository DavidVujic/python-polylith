from pathlib import Path

import tomlkit
from polylith import base, component, project, readme, repo
from polylith.development import create_development
from polylith.dirs import create_dir

template = """\
[tool.polylith]
namespace = "{namespace}"
"""


def get_namespace_from_config(path: Path) -> str:
    fullpath = path / repo.workspace_file

    content = fullpath.read_text()

    toml: dict = tomlkit.loads(content)

    return toml["tool"]["polylith"]["namespace"]


def create_workspace_config(path: Path, namespace: str) -> None:
    content: dict = tomlkit.loads(template.format(namespace=namespace))

    fullpath = path / repo.workspace_file

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(content))


def create_workspace(path: Path, namespace: str) -> None:
    create_dir(path, base.dir_name, keep=True)
    create_dir(path, component.dir_name, keep=True)
    create_dir(path, project.dir_name, keep=True)

    create_development(path, keep=True)

    create_workspace_config(path, namespace)

    readme.create_workspace_readme(path, namespace)
