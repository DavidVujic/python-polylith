import tomlkit
from polylith.project.create import create_project_toml


def test_create_project_toml():
    name = "unit test project"
    description = "this is a unit test"
    authors = ["one", "two", "three"]
    python_version = "something"

    template = 'x = "{name}{description}{authors}{python_version}"'

    data = {
        "name": name,
        "description": description,
        "authors": authors,
        "python_version": python_version,
    }

    res = create_project_toml(template, data)

    assert tomlkit.dumps(res) == f'x = "{name}{description}{authors}{python_version}"'
