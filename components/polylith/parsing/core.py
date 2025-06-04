import shutil
from pathlib import Path
from typing import Union

default_patterns = {
    "*.pyc",
    "__pycache__",
    ".venv",
    "__pypackages__",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "node_modules",
    ".git",
}


def copy_tree(source: str, destination: str, patterns: set) -> Path:
    ignore = shutil.ignore_patterns(*patterns)

    res = shutil.copytree(source, destination, ignore=ignore, dirs_exist_ok=True)

    return Path(res)


def copy_brick(
    source: str,
    brick: str,
    destination_dir: Path,
    exclude_patterns: Union[set, None] = None,
) -> Path:
    destination = Path(destination_dir / brick).as_posix()

    patterns = set().union(default_patterns, exclude_patterns or set())

    return copy_tree(source, destination, patterns)


def parse_brick_namespace_from_path(bricks: dict) -> str:
    parts = {str.split(v, "/")[0] for v in bricks.values()}

    return next(part for part in parts)
