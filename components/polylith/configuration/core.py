from pathlib import Path
from typing import List, Union

from polylith import repo


def get_namespace_from_config(path: Path) -> str:
    toml: dict = repo.load_workspace_config(path)

    return toml["tool"]["polylith"]["namespace"]


def get_git_tag_pattern(toml: dict) -> str:
    """Fallback git tag pattern configuration"""
    return toml["tool"]["polylith"]["git_tag_pattern"]


def get_tag_pattern_from_config(path: Path, key: Union[str, None]) -> Union[str, None]:
    toml: dict = repo.load_workspace_config(path)

    patterns = toml["tool"]["polylith"].get("tag", {}).get("patterns")

    if not key:
        return patterns["stable"] if patterns else get_git_tag_pattern(toml)

    return patterns.get(key)


def get_tag_sort_options_from_config(path: Path) -> List[str]:
    toml: dict = repo.load_workspace_config(path)

    options = toml["tool"]["polylith"].get("tag", {}).get("sorting")
    # Default sorting option
    if options is None:
        return ["-committerdate"]
    return options


def is_test_generation_enabled(path: Path) -> bool:
    toml: dict = repo.load_workspace_config(path)

    enabled = toml["tool"]["polylith"]["test"]["enabled"]
    return bool(enabled)


def is_readme_generation_enabled(path: Path) -> bool:
    toml: dict = repo.load_workspace_config(path)

    enabled = toml["tool"]["polylith"].get("resources", {}).get("brick_docs_enabled")
    return bool(enabled)


def get_theme_from_config(path: Path) -> str:
    toml: dict = repo.load_workspace_config(path)

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
