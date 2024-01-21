import shutil
from pathlib import Path
from typing import Any, Dict

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from polylith import repo, toml
from polylith.hatch import core


class PolylithBricksHook(BuildHookInterface):
    PLUGIN_NAME = "polylith-bricks"

    def initialize(self, _version: str, build_data: Dict[str, Any]) -> None:
        top_ns = self.config.get("top-namespace")
        work_dir = core.get_work_dir(self.config)
        pyproject = Path(f"{self.root}/{repo.default_toml}")

        data = toml.read_toml_document(pyproject)
        bricks = toml.get_project_packages_from_polylith_section(data)

        if not bricks:
            return

        if not top_ns:
            build_data["force_include"] = bricks
            return

        ns = core.parse_namespace(bricks)

        for source, brick in bricks.items():
            path = core.copy_brick(source, brick, work_dir)
            rewritten_bricks = core.rewrite_modules(path, ns, top_ns)

            for item in rewritten_bricks:
                print(f"Updated {item} with new top namespace for local imports.")

        key = work_dir.as_posix()
        build_data["force_include"][key] = top_ns

    def finalize(self, *args, **kwargs) -> None:
        work_dir = core.get_work_dir(self.config)

        if not work_dir.exists() or not work_dir.is_dir():
            return

        shutil.rmtree(work_dir.as_posix())
