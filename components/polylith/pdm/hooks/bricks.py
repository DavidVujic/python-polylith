import shutil
from pathlib import Path

from polylith import parsing, toml


def get_work_dir(config: dict) -> Path:
    build_config = config.get("tool", {}).get("pdm", {}).get("build", {})

    work_dir = build_config.get("work-dir", ".polylith_tmp")

    return Path(work_dir)


def build_initialize(config_data: dict) -> None:
    bricks = toml.get_project_packages_from_polylith_section(config_data)
    top_ns = toml.get_custom_top_namespace_from_polylith_section(config_data)
    work_dir = get_work_dir(config_data)

    if not bricks:
        print("No bricks found.")
        return

    if not top_ns:
        return  # TODO

    ns = parsing.parse_brick_namespace_from_path(bricks)

    for source, brick in bricks.items():
        path = parsing.copy_brick(source, brick, work_dir)
        rewritten_bricks = parsing.rewrite_modules(path, ns, top_ns)

        for item in rewritten_bricks:
            print(f"Updated {item} with new top namespace for local imports.")

    if not work_dir.exists() or not work_dir.is_dir():
        return

    shutil.rmtree(work_dir.as_posix())
