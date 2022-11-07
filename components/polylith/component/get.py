from collections.abc import Generator
from pathlib import Path

from polylith.repo import components_dir


def get_component_dirs(path: Path, top_dir, ns) -> Generator:
    component_dir = path / top_dir / ns

    return (f for f in component_dir.iterdir() if f.is_dir())


def get_components_data(path: Path, ns: str, top_dir: str = components_dir) -> list[dict]:
    dirs = get_component_dirs(path, top_dir, ns)

    return [{"name": d.name} for d in dirs]
