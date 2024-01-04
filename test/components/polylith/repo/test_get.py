from pathlib import Path

import tomlkit
from polylith import repo

poetry_toml = """\
[tool.poetry]
name = "hello world"
version = "0.1.0"
description = "describing the project"
authors = {authors}
license = "MIT"

packages = []

[tool.poetry.dependencies]
python = "^3.8"

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

pep_621_toml = """\
[project]
name = "hello world"
version = "0.1.0"
description = "describing the project"
authors = {authors}
license = ""
requires-python = "^3.8"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

path = Path.cwd()


def test_is_pep_621_compliant():
    assert repo.get.is_pep_621_compliant({"tool": {"poetry": {}}}) is False
    assert repo.get.is_pep_621_compliant({"project": {"hello": "world"}}) is True


def test_get_metadata_section():
    expected = {"hello": "world"}

    assert repo.get.get_metadata_section({"project": expected}) == expected
    assert repo.get.get_metadata_section({"tool": {"poetry": expected}}) == expected


def test_get_authors_for_poetry_toml(monkeypatch):
    expected = ["Unit Test"]
    data = poetry_toml.format(authors=expected)

    monkeypatch.setattr(repo.get, "get_pyproject_data", lambda _: tomlkit.loads(data))

    assert repo.get.get_authors(path) == expected


def test_get_authors_for_pep_621_compliant_toml(monkeypatch):
    authors = '[{name = "Unit Test", email = "the-email"}]'
    data = pep_621_toml.format(authors=authors)

    monkeypatch.setattr(repo.get, "get_pyproject_data", lambda _: tomlkit.loads(data))

    assert repo.get.get_authors(path) == [{"name": "Unit Test", "email": "the-email"}]


def test_get_python_version_for_poetry_toml(monkeypatch):
    data = pep_621_toml.format(authors=[])

    monkeypatch.setattr(repo.get, "get_pyproject_data", lambda _: tomlkit.loads(data))

    assert repo.get.get_python_version(path) == "^3.8"


def test_get_python_version_for_pep_621_compliant_toml(monkeypatch):
    data = pep_621_toml.format(authors=[])

    monkeypatch.setattr(repo.get, "get_pyproject_data", lambda _: tomlkit.loads(data))

    assert repo.get.get_python_version(path) == "^3.8"
