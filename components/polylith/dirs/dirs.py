from pathlib import Path
from typing import List

from polylith import configuration
from polylith.files import create_file
from polylith.repo import bases_dir, components_dir

keep_file_name = ".keep"


def create_dir(path: Path, dir_name: str, keep=False) -> Path:
    d = path / dir_name
    d.mkdir(parents=True)

    if keep:
        create_file(d, keep_file_name)

    return d


def is_brick_dir(p: Path) -> bool:
    return p.is_dir() and p.name not in {"__pycache__", ".venv", ".mypy_cache"}


def get_component_dirs(root: Path, top_dir, ns) -> list:
    theme = configuration.get_theme_from_config(root)
    dirs = top_dir if theme == "tdd" else f"{top_dir}/{ns}"

    component_dir = root / dirs

    if not component_dir.exists():
        return []

    return [f for f in component_dir.iterdir() if is_brick_dir(f)]


def get_components_data(
    root: Path, ns: str, top_dir: str = components_dir
) -> List[dict]:
    dirs = get_component_dirs(root, top_dir, ns)

    return [{"name": d.name} for d in dirs]


def get_bases_data(path: Path, ns: str) -> List[dict]:
    return get_components_data(path, ns, bases_dir)
