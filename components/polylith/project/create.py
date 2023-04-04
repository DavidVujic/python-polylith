from pathlib import Path
from typing import Union

import tomlkit
from polylith import repo
from polylith.dirs import create_dir
from polylith.repo import projects_dir

template = """\
[tool.poetry]
name = "{name}"
version = "0.1.0"
description = "{description}"
authors = {authors}
license = ""

packages = []

[tool.poetry.dependencies]
python = "{python_version}"

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""


def get_workspace_toml(path: Path) -> dict:
    with open(str(path / repo.default_toml), "r", errors="ignore") as f:
        data: dict = tomlkit.loads(f.read())

    return data


def create_project_toml(
    name: str, template: str, workspace_toml: dict, description: str
) -> tomlkit.TOMLDocument:
    authors = workspace_toml["tool"]["poetry"]["authors"]
    python_version = workspace_toml["tool"]["poetry"]["dependencies"]["python"]

    content = template.format(
        name=name,
        description=description,
        authors=authors,
        python_version=python_version,
    )

    return tomlkit.loads(content)


def create_project(
    path: Path, _namespace: str, name: str, description: Union[str, None]
) -> None:
    d = create_dir(path, f"{projects_dir}/{name}")

    workspace_toml = get_workspace_toml(path)
    project_toml = create_project_toml(
        name, template, workspace_toml, description or ""
    )

    fullpath = d / repo.default_toml

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(project_toml))
