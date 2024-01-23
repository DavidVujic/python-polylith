import tomlkit
from polylith import toml

namespace = "unittest"

poetry_toml = """\
[tool.poetry]
packages = [
    {include = "unittest/one",from = "../../bases"},
    {include = "unittest/two",from = "../../components"}
]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

hatch_toml = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.force-include]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

hatch_toml_alternative = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build]
something = "something"

[tool.polylith.bricks]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

hatch_toml_combined = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.force-include]
"something" = "else"

[tool.polylith.bricks]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

expected = [
    {"include": "unittest/one", "from": "../../bases"},
    {"include": "unittest/two", "from": "../../components"},
]


def test_get_poetry_package_includes():
    data = tomlkit.loads(poetry_toml)

    res = toml.get_project_package_includes(namespace, data)

    assert res == expected


def test_get_hatch_package_includes():
    data = tomlkit.loads(hatch_toml)

    res = toml.get_project_package_includes(namespace, data)

    assert res == expected


def test_get_hatch_package_includes_in_build_hook():
    data = tomlkit.loads(hatch_toml_alternative)

    res = toml.get_project_package_includes(namespace, data)

    assert res == expected


def test_get_hatch_package_includes_from_default_when_in_both():
    data = tomlkit.loads(hatch_toml_combined)

    res = toml.get_project_package_includes(namespace, data)

    assert res == expected
