from pathlib import Path
from typing import Union

import tomlkit
from poetry_polylith_plugin.components import bases, components, projects
from poetry_polylith_plugin.components.development import create_development
from poetry_polylith_plugin.components.dirs import create_dir

template = """\
[tool.polylith]
namespace = "{namespace}"
"""

workspace_file = "workspace.toml"
default_toml = "pyproject.toml"


def is_repo_root(cwd: Path) -> bool:
    fullpath = cwd / ".git"

    return fullpath.exists()


def find_upwards(cwd: Path, name: str) -> Union[Path, None]:
    if cwd == Path(cwd.root):
        return None

    fullpath = cwd / name

    if fullpath.exists():
        return fullpath

    if is_repo_root(cwd):
        return None

    return find_upwards(cwd.parent, name)


def find_upwards_dir(cwd: Path, name: str) -> Union[Path, None]:
    fullpath = find_upwards(cwd, name)

    return fullpath.parent if fullpath else None


def find_workspace_root(cwd: Path) -> Union[Path, None]:
    return find_upwards_dir(cwd, workspace_file)


def get_namespace_from_config(path: Path) -> str:
    fullpath = path / workspace_file

    content = fullpath.read_text()

    toml: dict = tomlkit.loads(content)

    return toml["tool"]["polylith"]["namespace"]


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
