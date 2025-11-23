from pathlib import Path

from polylith import environment


def build_initialize(config_data: dict, build_dir: Path, root: Path) -> None:
    environment.add_paths(config_data, build_dir, root)
