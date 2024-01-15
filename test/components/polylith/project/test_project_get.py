from polylith import project
import tomlkit

namespace = "unittest"

poetry_toml = """\
[tool.poetry]
packages = [
    {include = "unittest/one",from = "../../components"}
]
"""


hatch_toml = """\
[tool.hatch.build.force-include]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""


def test_get_poetry_package_includes():
    data = tomlkit.loads(poetry_toml)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == [{"include": "unittest/one", "from": "../../components"}]


def test_get_pep_621_includes():
    data = tomlkit.loads(hatch_toml)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == [
        {"include": "unittest/one", "from": "../../bases"},
        {"include": "unittest/two", "from": "../../components"},
    ]
