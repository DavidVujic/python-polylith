from pathlib import Path

import tomlkit
from poetry_polylith_plugin.components.dirs import create_dir

dir_name = "projects"

template = """\
[tool.poetry]
name = "{name}"
version = "0.1.0"
description = ""
authors = []
license = ""
readme = ""
packages = []

[tool.poetry.dependencies]
python = ""

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""


def get_pyproject_from_workspace(path: Path) -> dict:
    with open(str(path / "pyproject.toml"), "r") as f:
        data: dict = tomlkit.loads(f.read())

    return data


def create_project_pyproject(name) -> dict:
    return tomlkit.loads(template.format(name=name))


def pick_from_workspace(project_toml, workspace_toml):
    authors = workspace_toml["tool"]["poetry"]["authors"]
    python_version = workspace_toml["tool"]["poetry"]["dependencies"]["python"]

    project_toml["tool"]["poetry"]["authors"] = authors
    project_toml["tool"]["poetry"]["dependencies"]["python"] = python_version


def create_project(path: Path, namespace: str, name: str):
    d = create_dir(path, f"{dir_name}/{name}")

    workspace_toml = get_pyproject_from_workspace(path)
    project_toml = create_project_pyproject(name)

    pick_from_workspace(project_toml, workspace_toml)

    fullpath = d / "pyproject.toml"

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(project_toml))
