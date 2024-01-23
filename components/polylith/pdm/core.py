import shutil
from pathlib import Path

from polylith import parsing


def get_work_dir(config: dict) -> Path:
    build_config = config.get("tool", {}).get("pdm", {}).get("build", {})

    work_dir = build_config.get("work-dir", ".polylith_tmp")

    return Path(work_dir)


def copy_bricks_as_is(bricks: dict, build_dir: Path) -> None:
    for source, brick in bricks.items():
        parsing.copy_brick(source, brick, build_dir)


def copy_and_rewrite_bricks(
    bricks: dict, top_ns: str, work_dir: Path, build_dir: Path
) -> None:
    ns = parsing.parse_brick_namespace_from_path(bricks)

    for source, brick in bricks.items():
        path = parsing.copy_brick(source, brick, work_dir)
        rewritten_bricks = parsing.rewrite_modules(path, ns, top_ns)

        destination_dir = build_dir / top_ns
        parsing.copy_brick(path.as_posix(), brick, destination_dir)

        for item in rewritten_bricks:
            print(f"Updated {item} with new top namespace for local imports.")


def cleanup(work_dir: Path) -> None:
    if not work_dir.exists() or not work_dir.is_dir():
        return

    shutil.rmtree(work_dir.as_posix())
