from pathlib import Path

import tomlkit
from poetry_polylith_plugin.components import repo

template = """\
[tool.poetry]
name = "{name}"
version = "0.1.0"
description = ""
authors = {authors}
license = ""

packages = []

[tool.poetry.dependencies]
python = "{python_version}"

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""


def get_workspace_toml(path: Path) -> dict:
    with open(str(path / repo.default_toml), "r") as f:
        data: dict = tomlkit.loads(f.read())

    return data


def create_empty_toml(name: str, path: Path):
    workspace_toml = get_workspace_toml(repo.find_workspace_root(path))

    authors = workspace_toml["tool"]["poetry"]["authors"]
    python_version = workspace_toml["tool"]["poetry"]["dependencies"]["python"]

    content = template.format(name=name, authors=authors, python_version=python_version)

    toml_document = tomlkit.loads(content)

    fullpath = path / repo.default_toml

    with fullpath.open("w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(toml_document))
