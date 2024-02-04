from pathlib import Path
from typing import Set

from polylith import toml, workspace

defaults = {"bases", "components"}


def paths_from_config(root: Path, config_data: dict) -> Set[str]:
    ns = workspace.parser.get_namespace_from_config(root)
    packages = toml.get_project_package_includes(ns, config_data)

    return {p["from"] for p in packages}


def parse_paths(root: Path, config_data: dict) -> Set[str]:
    theme = workspace.parser.get_theme_from_config(root)

    paths = defaults if theme == "loose" else paths_from_config(root, config_data)

    return {(root / p).as_posix() for p in paths}


def write_pth_file(file_path: str, rows: Set[str]) -> None:
    with open(file_path, "w") as f:
        for row in rows:
            f.write(f"{row}\n")


def build_initialize(config_data: dict, build_dir: Path, root: Path) -> None:
    paths = parse_paths(root, config_data)

    if not paths:
        return

    filepath = build_dir / "polylith_workspace.pth"

    write_pth_file(filepath.as_posix(), paths)
