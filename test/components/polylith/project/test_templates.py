import pytest
import tomlkit
from polylith.project import templates

template_data = {
    "name": "a project",
    "description": "",
    "authors": "",
    "python_version": "3.12",
}


def with_optionals(description_field: str, authors_field: str) -> dict:
    return {
        **template_data,
        **{"description": description_field, "authors": authors_field},
    }


def with_poetry_optionals(description: str, author: str) -> dict:
    description_field = f'description = "{description}"'
    authors_field = f'authors = ["{author}"]'

    return with_optionals(description_field, authors_field)


def with_pep621_optionals(description: str, author: str) -> dict:
    description_field = f'description = "{description}"'
    authors_field = str.replace('authors = [{ name = "_AUTHOR_"}]', "_AUTHOR_", author)

    return with_optionals(description_field, authors_field)


def to_toml(template: str, data: dict):
    return tomlkit.loads(template.format(**data))


def test_poetry_template():
    data = to_toml(templates.poetry_pyproject, template_data)

    assert data["tool"]["poetry"] is not None
    assert data["tool"]["poetry"].get("authors") is None
    assert data["tool"]["poetry"].get("description") is None


def test_poetry_template_with_optionals():
    expected_description = "Hello world"
    expected_author = "Unit test"

    data = to_toml(
        templates.poetry_pyproject,
        with_poetry_optionals(expected_description, expected_author),
    )

    assert data["tool"]["poetry"]["description"] == expected_description
    assert data["tool"]["poetry"]["authors"] == [expected_author]


def test_hatch_template():
    data = to_toml(templates.hatch_pyproject, template_data)

    assert "hatch-polylith-bricks" in data["build-system"]["requires"]
    assert data["tool"]["hatch"]["build"]["hooks"]["polylith-bricks"] == {}
    assert data["tool"]["polylith"]["bricks"] == {}

    assert data["project"].get("description") is None
    assert data["project"].get("authors") is None


def test_pdm_template():
    data = to_toml(templates.pdm_pyproject, template_data)

    assert "pdm-polylith-bricks" in data["build-system"]["requires"]
    assert data["tool"]["polylith"]["bricks"] == {}

    assert data["project"].get("description") is None
    assert data["project"].get("authors") is None


@pytest.mark.parametrize("name", ["hatch", "pdm"])
def test_pep621_template_with_optionals(name):
    expected_description = "Hello world"
    expected_author = "Unit Test"

    template = {"hatch": templates.hatch_pyproject, "pdm": templates.pdm_pyproject}

    data = to_toml(
        template[name],
        with_pep621_optionals(expected_description, expected_author),
    )

    assert data["project"]["description"] == expected_description
    assert data["project"]["authors"] == [{"name": expected_author}]
