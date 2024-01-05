from polylith import project
import tomlkit

namespace = "unittest"

poetry_toml = """\
[tool.poetry]
packages = [
    {include = "unittest/one",from = "../../components"}
]
"""


pep_621_toml = """\
[project]
name = "unit test"
includes = ["../../components/unittest/one"]
"""


def test_get_poetry_package_includes():
    data = tomlkit.loads(poetry_toml)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == [{"include": "unittest/one", "from": "../../components"}]


def test_get_pep_621_includes():
    data = tomlkit.loads(pep_621_toml)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == [{"include": "unittest/one", "from": "../../components"}]
