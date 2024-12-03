import shutil
from pathlib import Path
from typing import Any, Dict, List

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from polylith import parsing, repo, toml
from polylith.hatch import core


def get_build_section(data: dict) -> dict:
    return data.get("tool", {}).get("hatch", {}).get("build", {})


def is_in_path(key: str, paths: List[str]) -> bool:
    return any(key.startswith(p) for p in paths)


def filter_dev_mode_bricks(data: dict, bricks: dict) -> dict:
    build_section = get_build_section(data)
    dev_mode_dirs = build_section.get("dev-mode-dirs")

    if not dev_mode_dirs:
        return bricks

    return {k: v for k, v in bricks.items() if not is_in_path(k, dev_mode_dirs)}


def filtered_bricks(data: dict, version: str) -> dict:
    bricks = toml.get_project_packages_from_polylith_section(data)

    if version == "editable":
        return filter_dev_mode_bricks(data, bricks)

    return bricks


class PolylithBricksHook(BuildHookInterface):
    PLUGIN_NAME = "polylith-bricks"

    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:
        include_key = "force_include"
        root = self.root
        pyproject = Path(f"{root}/{repo.default_toml}")

        data = toml.read_toml_document(pyproject)
        bricks = filtered_bricks(data, version)
        found_bricks = {k: v for k, v in bricks.items() if Path(f"{root}/{k}").exists()}

        if not bricks or not found_bricks:
            return

        top_ns = core.get_top_namespace(data, self.config)
        work_dir = core.get_work_dir(self.config)

        if not top_ns:
            build_data[include_key] = bricks
            return

        ns = parsing.parse_brick_namespace_from_path(bricks)

        for source, brick in bricks.items():
            path = parsing.copy_brick(source, brick, work_dir)
            rewritten_bricks = parsing.rewrite_modules(path, ns, top_ns)

            for item in rewritten_bricks:
                print(f"Updated {item} with new top namespace for local imports.")

        key = work_dir.as_posix()
        build_data[include_key][key] = top_ns

    def finalize(self, *args, **kwargs) -> None:
        work_dir = core.get_work_dir(self.config)

        if not work_dir.exists() or not work_dir.is_dir():
            return

        shutil.rmtree(work_dir.as_posix())
