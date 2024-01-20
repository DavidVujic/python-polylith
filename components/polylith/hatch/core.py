from pathlib import Path
from typing import List, Union

from polylith import parsing


def get_work_dir(config: dict) -> Path:
    work_dir = config.get("work_dir", ".tmp")

    return Path(work_dir)


def parse_namespace(bricks: dict) -> str:
    namespaces = parsing.parse_brick_namespace_from_path(bricks)

    return next(namespace for namespace in namespaces)


def copy_brick(source: str, brick: str, tmp_dir: Path) -> Path:
    destination = Path(tmp_dir / brick).as_posix()

    return parsing.copy_brick(source, destination)


def rewrite_module(module: Path, ns: str, top_ns: str) -> Union[str, None]:
    was_rewritten = parsing.rewrite_module(module, ns, top_ns)

    return f"{module.parent.name}/{module.name}" if was_rewritten else None


def rewrite_modules(path: Path, ns: str, top_ns: str) -> List[str]:
    """Rewrite modules in bricks with new top namespace

    returns a list of bricks that was rewritten
    """

    modules = path.glob("**/*.py")

    res = [rewrite_module(module, ns, top_ns) for module in modules]

    return [r for r in res if r]
