from pathlib import Path

import tomlkit
from polylith.project import get
import pytest


poetry_toml = """\
[tool.poetry]
name = "unit-test"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

pep_621_toml = """\
[project]
name = "unit-test"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""


def test_get_project_name_from_poetry_project():
    data = {"toml": tomlkit.loads(poetry_toml), "path": Path.cwd()}

    assert get.get_project_name_from_toml(data) == "unit-test"


def test_get_project_name_from_pep_621_project():
    data = {"toml": tomlkit.loads(pep_621_toml), "path": Path.cwd()}

    assert get.get_project_name_from_toml(data) == "unit-test"


def test_fetching_project_name_from_empty_project_raises_error():
    path = Path.cwd()

    data = {"toml": tomlkit.loads(""), "path": path}

    with pytest.raises(KeyError) as e:
        get.get_project_name_from_toml(data)

    assert str(path) in str(e.value)
