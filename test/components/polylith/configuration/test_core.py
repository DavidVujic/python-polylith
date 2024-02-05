from pathlib import Path
from typing import Tuple

import pytest
import tomlkit
from polylith.configuration import core

config_template = """
[tool.polylith]
namespace = "my_namespace"

[tool.polylith.structure]
theme = "{theme}"

[tool.polylith.tag.patterns]
stable = "stable-*"
release = "v[0-9]*"

[tool.polylith.test]
enabled = true
"""


@pytest.fixture
def use_fake(monkeypatch):
    def patch(theme: str):
        config = config_template.format(theme=theme)
        name = "_load_workspace_config"

        monkeypatch.setattr(core, name, lambda *args: tomlkit.loads(config))

    return patch


@pytest.fixture
def use_loose(use_fake):
    use_fake(theme="loose")


@pytest.fixture
def use_tdd(use_fake):
    use_fake(theme="tdd")


fake_path = Path.cwd()


def test_get_namespace(use_loose):
    res = core.get_namespace_from_config(fake_path)

    assert res == "my_namespace"


def test_get_tag_pattern(use_loose):
    stable = core.get_tag_pattern_from_config(fake_path, "stable")
    release = core.get_tag_pattern_from_config(fake_path, "release")

    assert stable == "stable-*"
    assert release == "v[0-9]*"


def test_is_test_generation_enabled(use_loose):
    res = core.is_test_generation_enabled(fake_path)

    assert res is True


def test_is_readme_generation_enabled(use_loose):
    res = core.is_readme_generation_enabled(fake_path)

    assert res is False


def test_get_theme(use_loose):
    res = core.get_theme_from_config(fake_path)

    assert res == "loose"


def _get_structure(path: Path) -> Tuple[str, str, str]:
    brick = core.get_brick_structure_from_config(path)
    test = core.get_tests_structure_from_config(path)
    resources = core.get_resources_structure_from_config(path)

    return brick, test, resources


def test_get_structure_for_loose_theme(use_loose):
    brick, test, resources = _get_structure(fake_path)

    expected = "{brick}/{namespace}/{package}"

    assert brick == expected
    assert test == f"test/{expected}"
    assert resources == expected


def test_get_structure_for_tdd_theme(use_tdd):
    brick, test, resources = _get_structure(fake_path)

    assert brick == "{brick}/{package}/src/{namespace}/{package}"
    assert test == "{brick}/{package}/test/{namespace}/{package}"
    assert resources == "{brick}/{package}"
