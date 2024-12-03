import tomlkit
from polylith.hatch.hooks.bricks import filtered_bricks

project_toml = """\
[tool.polylith.bricks]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

project_toml_dev_mode = """\
[tool.hatch.build]
dev-mode-dirs = ["../../components", "../../bases"]

[tool.polylith.bricks]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""


def test_filtered_bricks():
    data = tomlkit.loads(project_toml)

    expected = data["tool"]["polylith"]["bricks"]

    first = filtered_bricks(data, version="standard")
    second = filtered_bricks(data, version="editable")

    assert first == expected
    assert second == expected


def test_filtered_bricks_in_project_with_dev_mode_dirs():
    data = tomlkit.loads(project_toml_dev_mode)

    expected = data["tool"]["polylith"]["bricks"]

    first = filtered_bricks(data, version="standard")
    second = filtered_bricks(data, version="editable")

    assert first == expected
    assert second == {}
