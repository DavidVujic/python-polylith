import shutil
from pathlib import Path


def copy_brick(source: str, destination: str) -> Path:
    ignore = shutil.ignore_patterns(
        "*.pyc",
        "__pycache__",
        ".venv",
        ".mypy_cache",
        ".pytest_cache",
        "node_modules",
        ".git",
    )

    res = shutil.copytree(source, destination, ignore=ignore, dirs_exist_ok=True)

    return Path(res)


def parse_brick_namespace_from_path(bricks: dict) -> set:
    parts = {str.split(v, "/")[0] for v in bricks.values()}

    return parts
