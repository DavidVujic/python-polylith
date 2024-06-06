from functools import lru_cache
from pathlib import Path
from typing import List, Union

import tomlkit
from polylith import repo


@lru_cache
def _load_workspace_config(path: Path) -> tomlkit.TOMLDocument:
    fullpath = path / repo.workspace_file

    if not fullpath.exists():
        fullpath = path / repo.default_toml

    content = fullpath.read_text()

    return tomlkit.loads(content)


def get_namespace_from_config(path: Path) -> str:
    toml: dict = _load_workspace_config(path)

    return toml["tool"]["polylith"]["namespace"]


def get_git_tag_pattern(toml: dict) -> str:
    """Fallback git tag pattern configuration"""
    return toml["tool"]["polylith"]["git_tag_pattern"]


def get_tag_pattern_from_config(path: Path, key: Union[str, None]) -> str:
    toml: dict = _load_workspace_config(path)

    patterns = toml["tool"]["polylith"].get("tag", {}).get("patterns")

    return patterns[key or "stable"] if patterns else get_git_tag_pattern(toml)


def get_tag_sort_options_from_config(path: Path) -> List[str]:
    toml: dict = _load_workspace_config(path)

    options = toml["tool"]["polylith"].get("tag", {}).get("sorting")
    # Default sorting option
    if options is None:
        return ["-committerdate"]
    return options


def is_test_generation_enabled(path: Path) -> bool:
    toml: dict = _load_workspace_config(path)

    enabled = toml["tool"]["polylith"]["test"]["enabled"]
    return bool(enabled)


def is_readme_generation_enabled(path: Path) -> bool:
    toml: dict = _load_workspace_config(path)

    enabled = toml["tool"]["polylith"].get("resources", {}).get("brick_docs_enabled")
    return bool(enabled)


def get_theme_from_config(path: Path) -> str:
    toml: dict = _load_workspace_config(path)

    return toml["tool"]["polylith"]["structure"].get("theme") or "tdd"


def get_brick_structure_from_config(path: Path) -> str:
    theme = get_theme_from_config(path)

    if theme == "loose":
        return "{brick}/{namespace}/{package}"

    return "{brick}/{package}/src/{namespace}/{package}"


def get_tests_structure_from_config(path: Path) -> str:
    theme = get_theme_from_config(path)

    if theme == "loose":
        return "test/{brick}/{namespace}/{package}"

    return "{brick}/{package}/test/{namespace}/{package}"


def get_resources_structure_from_config(path: Path) -> str:
    theme = get_theme_from_config(path)

    if theme == "loose":
        return "{brick}/{namespace}/{package}"

    return "{brick}/{package}"
