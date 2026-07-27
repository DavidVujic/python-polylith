from pathlib import Path
from typing import Union

import tomlkit
from polylith.sync import update


def parse(data: Union[str, None]) -> dict:
    parsed = tomlkit.parse(data) if data else {}

    return parsed or {}


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

unsorted_packages = [
    {"include": "hello/c", "from": "components"},
    {"include": "hello/a", "from": "bases"},
    {"include": "hello/b", "from": "components"},
]

expected_sorted_pep621_bricks = {
    "bases/hello/first": "hello/first",
    "bases/hello/a": "hello/a",
    "components/hello/b": "hello/b",
    "components/hello/c": "hello/c",
}

poetry_project_data = """\
[tool.poetry]
packages = [{include = "hello/first", from = "bases"}]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""


hatchling_build_system = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

hatchling_project_data = """\
{build_system}

[tool.polylith.bricks]
"bases/hello/first" = "hello/first"
""".format(
    build_system=hatchling_build_system
)

hatch_specific_project_data = """\
{build_system}

[tool.hatch.build.force-include]
"bases/hello/first" = "hello/first"
""".format(
    build_system=hatchling_build_system
)


def test_generate_updated_poetry_project():
    data = tomlkit.parse(poetry_project_data)

    updated = update.generate_updated_project(data, packages[1:])

    res = parse(updated)["tool"]["poetry"]["packages"]

    assert res == packages


def test_generate_updated_poetry_project_with_the_bricks_to_update_sorted():
    data = tomlkit.parse(poetry_project_data)

    expected = [
        {"include": "hello/first", "from": "bases"},
        {"include": "hello/a", "from": "bases"},
        {"include": "hello/b", "from": "components"},
        {"include": "hello/c", "from": "components"},
    ]

    updated = update.generate_updated_project(data, unsorted_packages)

    res = parse(updated)["tool"]["poetry"]["packages"]

    assert res == expected


def test_generate_updated_hatch_project_with_existing_polylith_sections():
    data = tomlkit.parse(hatchling_project_data)

    updated = update.generate_updated_project(data, packages[1:])

    res = parse(updated)["tool"]["polylith"]["bricks"]

    assert res == expected_hatch_packages


def test_generate_updated_pep621_project_with_the_bricks_to_update_sorted():
    data = tomlkit.parse(hatchling_project_data)

    updated = update.generate_updated_project(data, unsorted_packages)

    res = parse(updated)["tool"]["polylith"]["bricks"]

    assert list(res.keys()) == list(expected_sorted_pep621_bricks.keys())


def test_generate_updated_hatch_project_with_missing_brick_config():
    data = tomlkit.parse(hatchling_build_system)

    updated = update.generate_updated_project(data, packages)

    res = parse(updated)["tool"]["polylith"]["bricks"]

    assert res == expected_hatch_packages


def test_generate_updated_hatch_project_with_existing_force_include():
    data = tomlkit.parse(hatch_specific_project_data)

    updated = update.generate_updated_project(data, packages[1:])

    res = parse(updated)["tool"]["hatch"]["build"]["force-include"]

    assert res == expected_hatch_packages


def test_generate_updated_hatch_project_force_include_with_sorted_bricks():
    data = tomlkit.parse(hatch_specific_project_data)

    updated = update.generate_updated_project(data, unsorted_packages)

    res = parse(updated)["tool"]["hatch"]["build"]["force-include"]

    assert list(res.keys()) == list(expected_sorted_pep621_bricks.keys())
