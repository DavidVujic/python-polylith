from collections.abc import Generator
from pathlib import Path

from polylith.component.constants import dir_name


def get_component_dirs(path: Path, top_dir) -> Generator:
    component_dir = path / top_dir

    return (f for f in component_dir.iterdir() if f.is_dir())


def dirs(path, ns) -> Generator:
    return (f.name for f in path.glob(f"{ns}/{path.name}") if f.is_dir())


def component_dirs(path: Path, ns: str) -> dict:
    src_dirs = dirs(path, ns)

    return {
        "name": path.name,
        "src": True if next(src_dirs, None) else False,
    }


def get_components_data(path: Path, ns: str, top_dir: str = dir_name) -> list[dict]:
    dirs = get_component_dirs(path, top_dir)

    return [component_dirs(d, ns) for d in dirs]
