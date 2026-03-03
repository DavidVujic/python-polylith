from pathlib import Path

from polylith import configuration, info
from polylith.dirs import create_dir
from polylith.files import create_file
from polylith.interface import create_interface
from polylith.readme import create_brick_readme


def validate(root: Path, namespace: str, name: str) -> None:
    bases = info.get_bases(root, namespace)
    components = info.get_components(root, namespace)

    if name in bases:
        message = f"{name} already exists in bases."
        raise ValueError(message)

    if name in components:
        message = f"{name} already exists in components."
        raise ValueError(message)


def create_brick(root: Path, options: dict) -> None:
    modulename = options["modulename"]
    package = options["package"]
    namespace = options["namespace"]

    validate(root, namespace, package)

    path_kwargs = {
        k: v for k, v in options.items() if k in {"brick", "namespace", "package"}
    }

    brick_structure = configuration.get_brick_structure_from_config(root)
    resources_structure = configuration.get_resources_structure_from_config(root)

    brick_path = brick_structure.format(**path_kwargs)
    resources_path = resources_structure.format(**path_kwargs)

    d = create_dir(root, brick_path)
    create_file(d, f"{modulename}.py")
    create_interface(d, options)

    if configuration.is_readme_generation_enabled(root):
        create_brick_readme(root / resources_path, options)
