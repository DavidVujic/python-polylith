from pathlib import Path

import tomlkit
from polylith.sync import update


def test_brick_to_pyproject_package():
    ns = "unit_test"
    brick = "greet"
    loose_theme = "loose"
    tdd_theme = "tdd"
    brick_path_dev = "components"
    brick_path_proj = "../../components"

    expected_dev = {"include": f"{ns}/{brick}", "from": brick_path_dev}
    expected_proj = {"include": f"{ns}/{brick}", "from": brick_path_proj}

    expected_tdd_dev = {"include": f"{ns}/{brick}", "from": f"components/{brick}/src"}
    expected_tdd_proj = {
        "include": f"{ns}/{brick}",
        "from": f"../../components/{brick}/src",
    }

    res_dev = update.to_package(ns, brick, brick_path_dev, loose_theme)
    res_proj = update.to_package(ns, brick, brick_path_proj, loose_theme)

    res_tdd_dev = update.to_package(ns, brick, brick_path_dev, tdd_theme)
    res_tdd_proj = update.to_package(ns, brick, brick_path_proj, tdd_theme)

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

    diff = {
        "name": "unit-test",
        "path": Path.cwd(),
        "is_project": False,
        "bases": {base},
        "components": {component},
    }

    res = update.to_packages(root, ns, diff)

    assert res == expected


packages = [
    {"include": "hello/first", "from": "bases"},
    {"include": "hello/second", "from": "components"},
    {"include": "hello/third", "from": "components"},
]


def test_generate_updated_project():
    data = tomlkit.parse(
        """\
[tool.poetry]
packages = [{include = "hello/first", from = "bases"}]
"""
    )

    updated = update.generate_updated_project(data, packages[1:])

    res = tomlkit.parse(updated)["tool"]["poetry"]["packages"]

    assert res == packages


def test_generate_updated_pep_621_ready_project():
    expected = [
        "bases/hello/first",
        "components/hello/second",
        "components/hello/third",
    ]

    data = tomlkit.parse(
        """\
[project]
name = "unit test"
includes = ["bases/hello/first"]
"""
    )

    updated = update.generate_updated_project(data, packages[1:])

    res = tomlkit.parse(updated)["project"]["includes"]

    assert res == expected
