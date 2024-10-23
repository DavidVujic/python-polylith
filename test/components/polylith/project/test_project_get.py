from pathlib import Path

import pytest
import tomlkit
from polylith.project import get

poetry_toml = """\
[tool.poetry]
name = "unit-test"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

poetry_pep_621_toml = """\
[tool.poetry]
packages = []

[project]
name = "unit-test"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

hatch_toml = """\
[project]
name = "unit-test"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

pdm_toml = """\
[project]
name = "unit-test"

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
"""


def test_get_project_name_from_poetry_project():
    data = {"toml": tomlkit.loads(poetry_toml), "path": Path.cwd()}

    assert get.get_project_name_from_toml(data) == "unit-test"


def test_get_project_name_from_pep_621_project():
    data = {"toml": tomlkit.loads(hatch_toml), "path": Path.cwd()}

    assert get.get_project_name_from_toml(data) == "unit-test"


def test_fetching_project_name_from_empty_project_raises_error():
    path = Path.cwd()

    data = {"toml": tomlkit.loads(""), "path": path}

    with pytest.raises(KeyError) as e:
        get.get_project_name_from_toml(data)

    assert str(path) in str(e.value)


def test_get_project_template_returns_poetry_template():
    data = tomlkit.loads(poetry_toml)

    res = get.guess_project_template(data)

    assert 'requires = ["poetry-core>=1.0.0"]' in res
    assert '[tool.poetry.dependencies]\npython = "{python_version}"' in res
    assert '[project]\nname = "{name}"' not in res


def test_get_project_template_returns_poetry_with_pep_621_support_template():
    data = tomlkit.loads(poetry_pep_621_toml)

    res = get.guess_project_template(data)

    assert 'requires = ["poetry-core>=1.0.0"]' in res
    assert '[project]\nname = "{name}"' in res


def test_get_project_template_returns_hatch_template():
    data = tomlkit.loads(hatch_toml)

    res = get.guess_project_template(data)

    assert 'requires = ["hatchling", "hatch-polylith-bricks"]' in res


def test_get_project_template_returns_pdm_template():
    data = tomlkit.loads(pdm_toml)

    res = get.guess_project_template(data)

    assert 'requires = ["pdm-backend", "pdm-polylith-bricks"]' in res
