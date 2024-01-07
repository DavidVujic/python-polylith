from pathlib import Path
from typing import List

import tomlkit
from polylith import repo, workspace


def transform_to_package(namespace: str, include: str) -> dict:
    path, _separator, brick = str.partition(include, f"/{namespace}/")

    return {"include": f"{namespace}/{brick}", "from": path}


def get_project_package_includes(namespace: str, data) -> List[dict]:
    if repo.is_pep_621_ready(data):
        includes = data["project"].get("includes", [])
        return [transform_to_package(namespace, include) for include in includes]

    return data["tool"]["poetry"].get("packages", [])


def get_project_name(data) -> str:
    if repo.is_pep_621_ready(data):
        return data["project"]["name"]

    return data["tool"]["poetry"]["name"]


def get_toml(path: Path) -> tomlkit.TOMLDocument:
    with path.open(encoding="utf-8", errors="ignore") as f:
        return tomlkit.loads(f.read())


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
    tomls = get_toml_files(root)
    namespace = workspace.parser.get_namespace_from_config(root)

    return [
        {
            "name": get_project_name(d["toml"]),
            "packages": get_project_package_includes(namespace, d["toml"]),
            "path": d["path"],
            "type": d["type"],
        }
        for d in tomls
    ]
