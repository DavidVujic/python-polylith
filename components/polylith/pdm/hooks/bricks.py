from pathlib import Path

from polylith import toml
from polylith.pdm import core


def build_initialize(root: Path, config_data: dict, build_dir: Path) -> None:
    bricks = toml.get_project_packages_from_polylith_section(config_data)
    found_bricks = {k: v for k, v in bricks.items() if Path(root / k).exists()}

    if not bricks or not found_bricks:
        return

    top_ns = toml.get_custom_top_namespace_from_polylith_section(config_data)
    work_dir = core.get_work_dir(config_data)

    if not top_ns:
        core.copy_bricks_as_is(bricks, build_dir)
    else:
        core.copy_and_rewrite(bricks, top_ns, work_dir, build_dir)
