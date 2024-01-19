import shutil
from pathlib import Path
from typing import Any, Dict

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from polylith import parsing, project, repo


def get_temp_dir(config: dict) -> Path:
    tmp_dir = config.get("tmp_dir", ".tmp")

    return Path(tmp_dir)


class PolylithBricksHook(BuildHookInterface):
    PLUGIN_NAME = "polylith-bricks"

    def initialize(self, version: str, build_data: Dict[str, Any]) -> None:
        top_ns = self.config.get("top_namespace")
        pyproject = Path(f"{self.root}/{repo.default_toml}")

        data = project.get_toml(pyproject)
        bricks = project.get_project_packages_from_polylith_section(data)

        if not bricks:
            return

        if not top_ns:
            build_data["force_include"] = bricks
            return

        namespaces = parsing.parse_brick_namespace_from_path(bricks)
        ns = next(namespace for namespace in namespaces)

        tmp_dir = get_temp_dir(self.config)

        for source, brick in bricks.items():
            destination = Path(tmp_dir / brick).as_posix()
            res = parsing.copy_brick(source, destination)

            modules = res.glob("**/*.py")

            for module in modules:
                was_rewritten = parsing.rewrite_module(module, ns, top_ns)

                if was_rewritten:
                    print(f"Updated {module.parent.name}/{module.name}.")

        key = tmp_dir.as_posix()
        build_data["force_include"][key] = top_ns

    def finalize(
        self, version: str, build_data: Dict[str, Any], artifact_path: str
    ) -> None:
        tmp_dir = get_temp_dir(self.config)

        if tmp_dir.exists() and tmp_dir.is_dir():
            shutil.rmtree(tmp_dir.as_posix())
