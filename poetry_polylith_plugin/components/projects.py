from pathlib import Path

import tomlkit
from poetry_polylith_plugin.components import repo
from poetry_polylith_plugin.components.dirs import create_dir

dir_name = "projects"

template = """\
[tool.poetry]
name = "{name}"
version = "0.1.0"
description = ""
authors = {authors}
license = ""
readme = ""
packages = []

[tool.poetry.dependencies]
python = "{python_version}"

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""


def get_workspace_toml(path: Path) -> dict:
    with open(str(path / repo.default_toml), "r") as f:
        data: dict = tomlkit.loads(f.read())

    return data


def create_project_toml(name, template, workspace_toml):
    authors = workspace_toml["tool"]["poetry"]["authors"]
    python_version = workspace_toml["tool"]["poetry"]["dependencies"]["python"]

    content = template.format(name=name, authors=authors, python_version=python_version)

    return tomlkit.loads(content)


def create_project(path: Path, namespace: str, name: str):
    d = create_dir(path, f"{dir_name}/{name}")

    workspace_toml = get_workspace_toml(path)
    project_toml = create_project_toml(name, template, workspace_toml)

    fullpath = d / repo.default_toml

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(project_toml))
