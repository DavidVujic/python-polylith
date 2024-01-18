import tomlkit
from polylith import project

namespace = "unittest"

poetry_toml = """\
[tool.poetry]
packages = [
    {include = "unittest/one",from = "../../bases"},
    {include = "unittest/two",from = "../../components"}
]
"""

hatch_toml = """\
[tool.hatch.build.force-include]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

hatch_toml_alternative = """\
[tool.hatch.build.hooks.targets.wheel.polylith.bricks]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

hatch_toml_combined = """\
[tool.hatch.build.force-include]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"

[tool.hatch.build.hooks.targets.wheel.polylith.bricks]
"something" = "else"
"""

expected = [
    {"include": "unittest/one", "from": "../../bases"},
    {"include": "unittest/two", "from": "../../components"},
]


def test_get_poetry_package_includes():
    data = tomlkit.loads(poetry_toml)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == expected


def test_get_hatch_package_includes():
    data = tomlkit.loads(hatch_toml)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == expected


def test_get_hatch_package_includes_in_build_hook():
    data = tomlkit.loads(hatch_toml_alternative)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == expected


def test_get_hatch_package_includes_from_default_when_in_both():
    data = tomlkit.loads(hatch_toml_combined)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == expected


def test_get_hatch_package_includes_lookup_with_unexpected_format():
    unexpected = """\
[tool.hatch.build.hooks.targets.wheel]
"polylith" = "this-is-unexpected"
"""
    data = tomlkit.loads(unexpected)

    res = project.get.get_project_package_includes(namespace, data)

    assert res == []
