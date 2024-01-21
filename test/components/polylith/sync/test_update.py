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

expected_hatch_packages = {
    "bases/hello/first": "hello/first",
    "components/hello/second": "hello/second",
    "components/hello/third": "hello/third",
}


def test_generate_updated_poetry_project():
    data = tomlkit.parse(
        """\
[tool.poetry]
packages = [{include = "hello/first", from = "bases"}]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""
    )

    updated = update.generate_updated_project(data, packages[1:])

    res = tomlkit.parse(updated)["tool"]["poetry"]["packages"]

    assert res == packages


def test_generate_updated_hatch_project():
    data = tomlkit.parse(
        """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.force-include]
"bases/hello/first" = "hello/first"
"""
    )

    updated = update.generate_updated_project(data, packages[1:])

    res = tomlkit.parse(updated)["tool"]["hatch"]["build"]["force-include"]

    assert res == expected_hatch_packages


def test_generate_updated_hatch_project_with_missing_build_config():
    data = tomlkit.parse(
        """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch]
hello = "world"
"""
    )

    updated = update.generate_updated_project(data, packages)

    res = tomlkit.parse(updated)["tool"]["hatch"]["build"]["force-include"]

    assert res == expected_hatch_packages


def test_generate_updated_hatch_project_with_missing_force_include_config():
    data = tomlkit.parse(
        """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build]
hello = "world"
"""
    )

    updated = update.generate_updated_project(data, packages)

    res = tomlkit.parse(updated)["tool"]["hatch"]["build"]["force-include"]

    assert res == expected_hatch_packages
