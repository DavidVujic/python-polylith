import shutil
from pathlib import Path
from typing import Any, Dict

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from polylith import parsing, project, repo


def get_work_dir(config: dict) -> Path:
    work_dir = config.get("work_dir", ".tmp")

    return Path(work_dir)


def parse_namespace(bricks: dict) -> str:
    namespaces = parsing.parse_brick_namespace_from_path(bricks)

    return next(namespace for namespace in namespaces)


def copy_brick(source: str, brick: str, tmp_dir: Path) -> Path:
    destination = Path(tmp_dir / brick).as_posix()

    return parsing.copy_brick(source, destination)


def rewrite_modules(path: Path, ns: str, top_ns: str) -> None:
    modules = path.glob("**/*.py")

    for module in modules:
        was_rewritten = parsing.rewrite_module(module, ns, top_ns)

        if was_rewritten:
            print(
                f"Updated {module.parent.name}/{module.name} with new top namespace for local imports."
            )


class PolylithBricksHook(BuildHookInterface):
    PLUGIN_NAME = "polylith-bricks"

    def initialize(self, _version: str, build_data: Dict[str, Any]) -> None:
        top_ns = self.config.get("top_namespace")
        work_dir = get_work_dir(self.config)
        pyproject = Path(f"{self.root}/{repo.default_toml}")

        data = project.get_toml(pyproject)
        bricks = project.get_project_packages_from_polylith_section(data)

        if not bricks:
            return

        if not top_ns:
            build_data["force_include"] = bricks
            return

        ns = parse_namespace(bricks)

        for source, brick in bricks.items():
            path = copy_brick(source, brick, work_dir)
            rewrite_modules(path, ns, top_ns)

        key = work_dir.as_posix()
        build_data["force_include"][key] = top_ns

    def finalize(self, *args, **kwargs) -> None:
        work_dir = get_work_dir(self.config)

        if not work_dir.exists() or not work_dir.is_dir():
            return

        shutil.rmtree(work_dir.as_posix())
