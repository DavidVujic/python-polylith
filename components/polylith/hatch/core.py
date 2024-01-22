from pathlib import Path
from typing import Union

from polylith import toml


def get_work_dir(config: dict) -> Path:
    work_dir = config.get("work-dir", ".polylith_tmp")

    return Path(work_dir)


def get_top_namespace(pyproject: dict, config: dict) -> Union[str, None]:
    top_ns = toml.get_custom_top_namespace_from_polylith_section(pyproject)

    return top_ns or config.get("top-namespace")
