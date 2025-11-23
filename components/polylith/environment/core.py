from pathlib import Path
from typing import Set

from polylith import configuration, toml


def paths_from_config(ns: str, data: dict) -> Set[str]:
    packages = toml.get_project_package_includes(ns, data)

    return {p["from"] for p in packages}


def parse_paths(root: Path, theme: str, ns: str, data: dict) -> Set[str]:
    defaults = {"bases", "components"}

    paths = defaults if theme == "loose" else paths_from_config(ns, data)

    return {(root / p).as_posix() for p in paths}


def write_pth_file(target_dir: Path, paths: Set[str]) -> None:
    filepath = target_dir / "polylith_workspace.pth"

    if filepath.exists():
        return

    with open(filepath, "w") as f:
        for p in paths:
            f.write(f"{p}\n")


def add_paths(config_data: dict, target_dir: Path, root: Path) -> None:
    theme = configuration.get_theme_from_config(root)
    ns = configuration.get_namespace_from_config(root)

    paths = parse_paths(root, theme, ns, config_data)

    if not paths:
        return

    write_pth_file(target_dir, paths)
