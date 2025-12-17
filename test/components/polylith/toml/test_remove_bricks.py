import tomlkit

from polylith import toml


def test_remove_brick_from_poetry_packages():
    data = tomlkit.parse(
        """\
[tool.poetry]
packages = [
  {include = "test_space/hello", from = "components"},
  {include = "test_space/world", from = "components"},
]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    )

    changed = toml.remove_brick_from_project_packages(
        data, "test_space/world", "components"
    )

    assert changed is True
    res = data["tool"]["poetry"]["packages"]
    assert len(res) == 1
    assert res[0]["include"] == "test_space/hello"


def test_remove_brick_from_polylith_bricks_section():
    data = tomlkit.parse(
        """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.polylith.bricks]
"components/test_space/world" = "test_space/world"
"components/test_space/hello" = "test_space/hello"
"bases/test_space/world" = "test_space/world"
"""
    )

    changed = toml.remove_brick_from_project_packages(
        data, "test_space/world", "components"
    )

    assert changed is True
    bricks = data["tool"]["polylith"]["bricks"]
    assert "components/test_space/world" not in bricks
    assert "bases/test_space/world" in bricks


def test_remove_brick_from_force_include_section():
    data = tomlkit.parse(
        """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.force-include]
"components/test_space/world" = "test_space/world"
"components/test_space/hello" = "test_space/hello"
"""
    )

    changed = toml.remove_brick_from_project_packages(
        data, "test_space/world", "components"
    )

    assert changed is True
    include = data["tool"]["hatch"]["build"]["force-include"]
    assert "components/test_space/world" not in include
    assert "components/test_space/hello" in include
