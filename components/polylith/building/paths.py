from pathlib import Path
from typing import Union

from polylith import toml


def get_work_dir(options: dict) -> Path:
    work_dir = options.get("work-dir", ".polylith_tmp")

    return Path(work_dir)


def calculate_root_dir(bricks: dict) -> Union[str, None]:
    brick_path = next((v for v in bricks.values()), None)

    return str.split(brick_path, "/")[0] if brick_path else None


def calculate_destination_dir(data: dict) -> Union[Path, None]:
    bricks = toml.get_project_packages_from_polylith_section(data)

    if not bricks:
        return None

    custom_top_ns = toml.get_custom_top_namespace_from_polylith_section(data)

    if custom_top_ns:
        return Path(custom_top_ns)

    root = calculate_root_dir(bricks)

    return Path(root) if root else None
