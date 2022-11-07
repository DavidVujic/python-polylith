from pathlib import Path

import tomlkit
from polylith import repo


def _load_workspace_config(path: Path) -> tomlkit.TOMLDocument:
    fullpath = path / repo.workspace_file

    content = fullpath.read_text()

    return tomlkit.loads(content)


def get_namespace_from_config(path: Path) -> str:
    toml: dict = _load_workspace_config(path)

    return toml["tool"]["polylith"]["namespace"]


def get_brick_structure_from_config(path: Path) -> str:
    toml: dict = _load_workspace_config(path)

    return toml["tool"]["polylith"]["structure"]["bricks"]


def get_test_template_from_config(path: Path) -> str:
    toml: dict = _load_workspace_config(path)

    return toml["tool"]["polylith"]["test"]["template"]


def is_test_generation_enabled(path: Path) -> bool:
    toml: dict = _load_workspace_config(path)

    enabled = toml["tool"]["polylith"]["test"]["enabled"]
    return bool(enabled)


def get_tests_structure_from_config(path: Path) -> str:
    toml: dict = _load_workspace_config(path)

    return toml["tool"]["polylith"]["structure"]["tests"]
