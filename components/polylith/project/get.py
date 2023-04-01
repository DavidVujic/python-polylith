from pathlib import Path
from typing import List

import tomlkit
from polylith.repo import default_toml


def get_project_package_includes(data) -> List[dict]:
    return data["tool"]["poetry"].get("packages", [])


def get_project_name(data) -> str:
    return data["tool"]["poetry"]["name"]


def get_toml(path: Path) -> tomlkit.TOMLDocument:
    with path.open(encoding="utf-8", errors="ignore") as f:
        return tomlkit.loads(f.read())


def get_project_files(root: Path) -> dict:
    projects = sorted(root.glob(f"projects/**/{default_toml}"))
    development = Path(root / default_toml)

    proj = {"projects": projects}
    dev = {"development": [development]}

    return {**proj, **dev}


def toml_data(path: Path, project_type: str) -> dict:
    return {"toml": get_toml(path), "path": path.parent, "type": project_type}


def get_toml_files(root: Path) -> List[dict]:
    project_files = get_project_files(root)

    proj = [toml_data(p, "project") for p in project_files["projects"]]
    dev = [toml_data(d, "development") for d in project_files["development"]]

    return proj + dev


def get_packages_for_projects(root: Path) -> List[dict]:
    tomls = get_toml_files(root)

    return [
        {
            "name": get_project_name(d["toml"]),
            "packages": get_project_package_includes(d["toml"]),
            "path": d["path"],
            "type": d["type"],
        }
        for d in tomls
    ]
