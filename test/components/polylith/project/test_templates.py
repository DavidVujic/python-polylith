import tomlkit
from polylith.project import templates


template_data = {
    "name": "a project",
    "description": "",
    "authors": "",
    "python_version": "3.12",
}


def test_poetry_template():
    data = tomlkit.loads(templates.poetry_pyproject.format(**template_data))

    assert data["tool"]["poetry"] is not None
    assert data["tool"]["poetry"].get("authors") is None
    assert data["tool"]["poetry"].get("description") is None


def test_poetry_template_with_optionals():
    expected_description = "Hello world"
    expected_authors = ["Unit test"]

    description_field = f'description = "{expected_description}"'
    authors_field = f"authors = {expected_authors}"

    with_optionals = {
        **template_data,
        **{"description": description_field, "authors": authors_field},
    }
    data = tomlkit.loads(templates.poetry_pyproject.format(**with_optionals))

    assert data["tool"]["poetry"]["description"] == expected_description
    assert data["tool"]["poetry"]["authors"] == expected_authors


def test_hatch_template():
    data = tomlkit.loads(templates.hatch_pyproject.format(**template_data))

    assert "hatch-polylith-bricks" in data["build-system"]["requires"]
    assert data["tool"]["hatch"]["build"]["hooks"]["polylith-bricks"] == {}
    assert data["tool"]["polylith"]["bricks"] == {}

    assert data["project"].get("description") is None
    assert data["project"].get("authors") is None


def test_hatch_template_with_optionals():
    expected_description = "Hello world"

    description_field = f'description = "{expected_description}"'
    authors_field = 'authors = [{ name = "Unit Test"}]'

    with_optionals = {
        **template_data,
        **{"description": description_field, "authors": authors_field},
    }
    data = tomlkit.loads(templates.hatch_pyproject.format(**with_optionals))

    assert data["project"]["description"] == expected_description
    assert data["project"]["authors"] == [{"name": "Unit Test"}]


def test_pdm_template():
    data = tomlkit.loads(templates.pdm_pyproject.format(**template_data))

    assert "pdm-polylith-bricks" in data["build-system"]["requires"]
    assert data["tool"]["polylith"]["bricks"] == {}

    assert data["project"].get("description") is None
    assert data["project"].get("authors") is None


def test_pdm_template_with_optionals():
    expected_description = "Hello world"

    description_field = f'description = "{expected_description}"'
    authors_field = 'authors = [{ name = "Unit Test"}]'

    with_optionals = {
        **template_data,
        **{"description": description_field, "authors": authors_field},
    }
    data = tomlkit.loads(templates.pdm_pyproject.format(**with_optionals))

    assert data["project"]["description"] == expected_description
    assert data["project"]["authors"] == [{"name": "Unit Test"}]
