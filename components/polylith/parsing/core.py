import shutil
from pathlib import Path


def copy_tree(source: str, destination: str) -> Path:
    ignore = shutil.ignore_patterns(
        "*.pyc",
        "__pycache__",
        ".venv",
        "__pypackages__",
        ".mypy_cache",
        ".pytest_cache",
        "node_modules",
        ".git",
    )

    res = shutil.copytree(source, destination, ignore=ignore, dirs_exist_ok=True)

    return Path(res)


def copy_brick(source: str, brick: str, destination_dir: Path) -> Path:
    destination = Path(destination_dir / brick).as_posix()

    return copy_tree(source, destination)


def parse_brick_namespace_from_path(bricks: dict) -> str:
    parts = {str.split(v, "/")[0] for v in bricks.values()}

    return next(part for part in parts)
