import re
from functools import lru_cache
from pathlib import Path
from typing import Any, List

import tomlkit
from polylith import repo, workspace


def transform_to_package(namespace: str, include: str) -> dict:
    path, _separator, brick = str.partition(include, f"/{namespace}/")

    return {"include": f"{namespace}/{brick}", "from": path}


def find_by_key(data: dict, key: str) -> Any:
    if key in data.keys():
        return data[key]

    filtered = {k: v for k, v in data.items() if isinstance(data[k], dict)}

    res = (find_by_key(data[k], key) for k in filtered.keys())

    return next((r for r in res if r), None)


def get_hatch_project_packages(data) -> dict:
    build_data = data["tool"]["hatch"].get("build", {})

    force_included = build_data.get("force-include")

    if force_included:
        return force_included

    found = find_by_key(build_data, "polylith")

    return found.get("bricks", {}) if isinstance(found, dict) else {}


def get_project_package_includes(namespace: str, data) -> List[dict]:
    if repo.is_poetry(data):
        return data["tool"]["poetry"].get("packages", [])

    if repo.is_hatch(data):
        includes = get_hatch_project_packages(data)

        return [transform_to_package(namespace, key) for key in includes.keys()]

    return []


def get_project_name(data) -> str:
    if repo.is_pep_621_ready(data):
        return data["project"]["name"]

    return data["tool"]["poetry"]["name"]


def get_project_dependencies(data) -> dict:
    if repo.is_poetry(data):
        deps = data["tool"]["poetry"].get("dependencies", [])

        items = set(deps.keys())
    else:
        deps = data["project"].get("dependencies", [])

        items = {re.split(r"[\^~=!<>]", dep)[0] for dep in deps}

    return {"items": items, "source": repo.default_toml}


@lru_cache
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
            "deps": get_project_dependencies(d["toml"]),
        }
        for d in tomls
    ]
