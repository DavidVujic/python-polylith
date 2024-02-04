from pathlib import Path
from typing import Set

from polylith import toml, workspace


def paths_from_config(root: Path, ns: str, data: dict) -> Set[str]:
    packages = toml.get_project_package_includes(ns, data)

    return {p["from"] for p in packages}


def parse_paths(root: Path, theme: str, ns: str, data: dict) -> Set[str]:
    defaults = {"bases", "components"}

    paths = defaults if theme == "loose" else paths_from_config(root, ns, data)

    return {(root / p).as_posix() for p in paths}


def write_pth_file(build_dir: Path, paths: Set[str]) -> None:
    filepath = build_dir / "polylith_workspace.pth"

    with open(filepath, "w") as f:
        for p in paths:
            f.write(f"{p}\n")


def build_initialize(config_data: dict, build_dir: Path, root: Path) -> None:
    theme = workspace.parser.get_theme_from_config(root)
    ns = workspace.parser.get_namespace_from_config(root)

    paths = parse_paths(root, theme, ns, config_data)

    if not paths:
        return

    write_pth_file(build_dir, paths)
