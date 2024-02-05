from functools import lru_cache
from pathlib import Path
from typing import List

import tomlkit
from polylith import configuration, repo, toml


def get_project_name(data) -> str:
    if repo.is_pep_621_ready(data):
        return data["project"]["name"]

    return data["tool"]["poetry"]["name"]


@lru_cache
def get_toml(path: Path) -> tomlkit.TOMLDocument:
    return toml.read_toml_document(path)


def get_project_files(root: Path) -> dict:
    projects = sorted(root.glob(f"projects/**/{repo.default_toml}"))
    development = Path(root / repo.default_toml)

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
    toml_files = get_toml_files(root)
    namespace = configuration.get_namespace_from_config(root)

    return [
        {
            "name": get_project_name(d["toml"]),
            "packages": toml.get_project_package_includes(namespace, d["toml"]),
            "path": d["path"],
            "type": d["type"],
            "deps": toml.get_project_dependencies(d["toml"]),
        }
        for d in toml_files
    ]
