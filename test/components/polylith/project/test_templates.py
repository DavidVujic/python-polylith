import tomlkit
from polylith.project import templates


template_data = {
    "name": "a project",
    "description": "a description",
    "authors": [],
    "python_version": "3.12",
}


def test_poetry_template():
    data = tomlkit.loads(templates.poetry_pyproject.format(**template_data))

    assert data["tool"]["poetry"] is not None


def test_hatch_template():
    data = tomlkit.loads(templates.hatch_pyproject.format(**template_data))

    assert "hatch-polylith-bricks" in data["build-system"]["requires"]
    assert data["tool"]["hatch"]["build"]["hooks"]["polylith-bricks"] == {}
    assert data["tool"]["polylith"]["bricks"] == {}


def test_pdm_template():
    data = tomlkit.loads(templates.pdm_pyproject.format(**template_data))

    assert "pdm-polylith-bricks" in data["build-system"]["requires"]
    assert data["tool"]["polylith"]["bricks"] == {}
