from pathlib import Path
from typing import Union

from polylith import building, toml


def get_work_dir(config: dict) -> Path:
    return building.get_work_dir(config)


def get_top_namespace(pyproject: dict, config: dict) -> Union[str, None]:
    top_ns = toml.get_custom_top_namespace_from_polylith_section(pyproject)

    return top_ns or config.get("top-namespace")
