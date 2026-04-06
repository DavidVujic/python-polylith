from pathlib import Path
from typing import List, Set, Union

from polylith import repo


def get_polylith_config(path: Path) -> dict:
    toml: dict = repo.load_workspace_config(path)

    conf = toml.get("tool", {}).get("polylith")

    if not conf:
        message = "Cannot find a [tool.polylith] configuration."
        raise ValueError(message)

    return conf


def get_namespace_from_config(path: Path) -> str:
    conf = get_polylith_config(path)
    ns = conf.get("namespace")

    if not ns:
        message = "Cannot find a [tool.polylith.namespace] section."
        raise ValueError(message)

    return ns


def get_tag_pattern_from_config(path: Path, key: Union[str, None]) -> Union[str, None]:
    conf = get_polylith_config(path)

    patterns = conf.get("tag", {}).get("patterns")
    fallback = conf.get("git_tag_pattern")

    if not key:
        stable = patterns.get("stable") if patterns else None
        return stable or fallback

    return patterns.get(key) if patterns else None


def get_tag_sort_options_from_config(path: Path) -> List[str]:
    conf = get_polylith_config(path)

    options = conf.get("tag", {}).get("sorting")
    # Default sorting option
    if options is None:
        return ["-committerdate"]
    return options


def is_test_generation_enabled(path: Path) -> bool:
    conf = get_polylith_config(path)
    enabled = conf.get("test", {}).get("enabled")

    return bool(enabled)


def is_readme_generation_enabled(path: Path) -> bool:
    conf = get_polylith_config(path)
    enabled = conf.get("resources", {}).get("brick_docs_enabled")

    return bool(enabled)


def get_theme_from_config(path: Path) -> str:
    conf = get_polylith_config(path)

    return conf.get("structure", {}).get("theme") or "tdd"


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


def get_output_dir(path: Path, command_name: str) -> str:
    conf = get_polylith_config(path)

    key = "output"

    commands = conf.get("commands") or {}
    command = commands.get(command_name) or {}

    output = command.get(key) or commands.get(key)
    fallback = f"{repo.development_dir}/poly"

    return output or fallback


def get_projects_config(path: Path) -> dict:
    conf = get_polylith_config(path)

    return conf.get("projects", {})


def get_project_alias_from_config(path: Path, project_name: str) -> Union[str, None]:
    projects_conf = get_projects_config(path)
    alias = projects_conf.get("alias", {})

    return alias.get(project_name)


def get_project_groups_from_config(path: Path, project_name: str) -> Set[str]:
    projects_conf = get_projects_config(path)

    groups = projects_conf.get("groups") or {}

    if not groups:
        return set()

    return {k for k, v in groups.items() if project_name in v}
