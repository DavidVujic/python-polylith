from pathlib import Path

import tomlkit
from poetry_polylith_plugin.components import bases, components, projects
from poetry_polylith_plugin.components.development import create_development
from poetry_polylith_plugin.components.dirs import create_dir

template = """\
[tool.polylith]
namespace = "{namespace}"
"""


def create_workspace_config(path: Path, namespace: str) -> None:
    content: dict = tomlkit.loads(template.format(namespace=namespace))

    fullpath = path / "workspace.toml"

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(content))


def create_workspace(path: Path, namespace: str):
    create_dir(path, bases.dir_name, keep=True)
    create_dir(path, components.dir_name, keep=True)
    create_dir(path, projects.dir_name, keep=True)

    create_development(path, keep=True)

    create_workspace_config(path, namespace)
