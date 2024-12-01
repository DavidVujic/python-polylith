from pathlib import Path

from polylith import building


def get_work_dir(config: dict) -> Path:
    build_config = config.get("tool", {}).get("pdm", {}).get("build", {})

    return building.get_work_dir(build_config)


def copy_bricks_as_is(bricks: dict, build_dir: Path) -> None:
    building.copy_bricks_as_is(bricks, build_dir)


def copy_and_rewrite(
    bricks: dict, top_ns: str, work_dir: Path, build_dir: Path
) -> None:
    rewritten = building.copy_and_rewrite_bricks(bricks, top_ns, work_dir, build_dir)

    for item in rewritten:
        print(f"Updated {item} with new top namespace for local imports.")

    building.cleanup(work_dir)
