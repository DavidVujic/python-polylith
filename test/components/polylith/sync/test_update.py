import tomlkit
from polylith.sync import update


def test_brick_to_pyproject_package():
    ns = "unit_test"
    brick = "greet"
    brick_folder = "components"

    expected_dev = {"include": f"{ns}/{brick}", "from": brick_folder}
    expected_proj = {"include": f"{ns}/{brick}", "from": f"../../{brick_folder}"}

    res_dev = update.to_package(ns, brick, brick_folder, False)
    res_proj = update.to_package(ns, brick, brick_folder, True)

    assert res_dev == expected_dev
    assert res_proj == expected_proj


def test_bricks_to_pyproject_packages():
    ns = "unit_test"
    base = "hello"
    component = "world"

    expected = [
        {"include": f"{ns}/{base}", "from": "bases"},
        {"include": f"{ns}/{component}", "from": "components"},
    ]

    res = update.to_packages(ns, {base}, {component}, False)

    assert res == expected


def test_generate_updated_project():
    expected = [
        {"include": "hello/first", "from": "bases"},
        {"include": "hello/second", "from": "bases"},
        {"include": "hello/third", "from": "components"},
    ]

    data = tomlkit.parse(
        """\
[tool.poetry]
packages = [{include = "hello/first", from = "bases"}]
"""
    )

    updated = update.generate_updated_project(data, expected[1:])

    res = tomlkit.parse(updated)["tool"]["poetry"]["packages"]

    assert res == expected
