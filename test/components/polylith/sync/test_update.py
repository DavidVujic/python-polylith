from pathlib import Path

import tomlkit
from polylith.sync import update


def test_brick_to_pyproject_package():
    ns = "unit_test"
    brick = "greet"
    brick_type = "components"
    loose_theme = "loose"
    tdd_theme = "tdd"

    expected_dev = {"include": f"{ns}/{brick}", "from": brick_type}
    expected_proj = {"include": f"{ns}/{brick}", "from": f"../../{brick_type}"}

    expected_tdd_dev = {"include": f"{ns}/{brick}", "from": f"{brick_type}/{brick}/src"}
    expected_tdd_proj = {
        "include": f"{ns}/{brick}",
        "from": f"../../{brick_type}/{brick}/src",
    }

    res_dev = update.to_package(ns, brick, brick_type, loose_theme, False)
    res_proj = update.to_package(ns, brick, brick_type, loose_theme, True)

    res_tdd_dev = update.to_package(ns, brick, brick_type, tdd_theme, False)
    res_tdd_proj = update.to_package(ns, brick, brick_type, tdd_theme, True)

    assert res_dev == expected_dev
    assert res_proj == expected_proj

    assert res_tdd_dev == expected_tdd_dev
    assert res_tdd_proj == expected_tdd_proj


def test_bricks_to_pyproject_packages():
    root = Path.cwd()
    ns = "unit_test"
    base = "hello"
    component = "world"

    expected = [
        {"include": f"{ns}/{base}", "from": "bases"},
        {"include": f"{ns}/{component}", "from": "components"},
    ]

    res = update.to_packages(root, ns, {base}, {component}, False)

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
