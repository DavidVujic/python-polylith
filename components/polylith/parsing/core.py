import fnmatch
import shutil
from pathlib import Path
from typing import List, Set, Union

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
    ".pixi",
}


def is_match(root: Path, pattern: str, name: str, current: Path) -> bool:
    path_name = (current / name).relative_to(root).as_posix()

    return any(fnmatch.fnmatch(n, pattern) for n in [path_name, name])


def any_match(root: Path, patterns: set, name: str, current: Path) -> bool:
    return any(is_match(root, pattern, name, current) for pattern in patterns)


def ignore_paths(root: Path, patterns: Set[str]):
    def fn(current_path: str, names: List[str]):
        current = Path(current_path).resolve()

        return {name for name in names if any_match(root, patterns, name, current)}

    return fn


def calculate_root(current_path: str) -> Path:
    relative = Path(current_path)

    parts = [p for p in relative.parts if p != ".."]
    relative_path = "/".join(parts)

    root = relative.resolve().as_posix().replace(relative_path, "")

    return Path(root)


def copy_tree(source: str, destination: str, patterns: Set[str]) -> Path:
    root = calculate_root(source)

    is_paths = any("/" in p for p in patterns)
    fn = ignore_paths(root, patterns) if is_paths else shutil.ignore_patterns(*patterns)

    res = shutil.copytree(source, destination, ignore=fn, dirs_exist_ok=True)

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
