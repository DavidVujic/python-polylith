import tomlkit
from polylith.project.create import create_project_toml


def test_create_project_toml():
    name = "unit test project"
    description = "this is a unit test"
    authors = ["one", "two", "three"]
    python_version = "something"

    template = 'x = "{name}{description}{authors}{python_version}"'

    res = create_project_toml(name, template, authors, python_version, description)

    assert tomlkit.dumps(res) == f'x = "{name}{description}{authors}{python_version}"'
