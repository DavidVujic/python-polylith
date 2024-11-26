import operator
import shutil
from functools import reduce
from pathlib import Path
from typing import List

from polylith import parsing


def copy_bricks_as_is(bricks: dict, build_dir: Path) -> None:
    for source, brick in bricks.items():
        parsing.copy_brick(source, brick, build_dir)


def copy_and_rewrite(source: str, brick: str, options: dict) -> List[str]:
    work_dir = options["work_dir"]
    build_dir = options["build_dir"]
    top_ns = options["top_ns"]
    ns = options["ns"]

    path = parsing.copy_brick(source, brick, work_dir)
    rewritten = parsing.rewrite_modules(path, ns, top_ns)

    destination_dir = build_dir / top_ns
    parsing.copy_brick(path.as_posix(), brick, destination_dir)

    return rewritten


def copy_and_rewrite_bricks(
    bricks: dict, top_ns: str, work_dir: Path, build_dir: Path
) -> List[str]:
    ns = parsing.parse_brick_namespace_from_path(bricks)

    options = {"ns": ns, "top_ns": top_ns, "work_dir": work_dir, "build_dir": build_dir}

    matrix = [
        copy_and_rewrite(source, brick, options) for source, brick in bricks.items()
    ]

    rewritten: List[str] = reduce(operator.iadd, matrix, [])

    return sorted(rewritten)


def cleanup(work_dir: Path) -> None:
    if not work_dir.exists() or not work_dir.is_dir():
        return

    shutil.rmtree(work_dir.as_posix())
