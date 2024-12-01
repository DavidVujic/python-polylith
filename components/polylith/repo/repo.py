from functools import lru_cache
from pathlib import Path
from typing import Union

import tomlkit

workspace_file = "workspace.toml"
root_file = ".git"
default_toml = "pyproject.toml"
readme_file = "README.md"

bases_dir = "bases"
components_dir = "components"
projects_dir = "projects"
development_dir = "development"


def load_content(fullpath: Path) -> tomlkit.TOMLDocument:
    content = fullpath.read_text()

    return tomlkit.loads(content)


@lru_cache
def load_root_project_config(path: Path) -> tomlkit.TOMLDocument:
    fullpath = path / default_toml

    if not fullpath.exists():
        return tomlkit.TOMLDocument()

    return load_content(fullpath)


def has_workspace_config(data: tomlkit.TOMLDocument) -> bool:
    ns = data.get("tool", {}).get("polylith", {}).get("namespace")

    return True if ns else False


@lru_cache
def load_workspace_config(path: Path) -> tomlkit.TOMLDocument:
    fullpath = path / workspace_file

    if fullpath.exists():
        content = load_content(fullpath)

        if has_workspace_config(content):
            return content

    return load_root_project_config(path)


def is_drive_root(cwd: Path) -> bool:
    return cwd == Path(cwd.root) or cwd == cwd.parent


def is_repo_root(cwd: Path) -> bool:
    fullpath = cwd / root_file

    return fullpath.exists()


def is_python_workspace_root(path: Path) -> bool:
    data = load_root_project_config(path)

    return has_workspace_config(data)


def find_upwards(cwd: Path, name: str) -> Union[Path, None]:
    if is_drive_root(cwd):
        return None

    fullpath = cwd / name

    if fullpath.exists():
        if name == workspace_file:
            return fullpath

        return fullpath if is_python_workspace_root(cwd) else None

    if is_repo_root(cwd):
        return None

    return find_upwards(cwd.parent, name)


def find_upwards_dir(cwd: Path, name: str) -> Union[Path, None]:
    fullpath = find_upwards(cwd, name)

    return fullpath.parent if fullpath else None


def find_workspace_root(cwd: Path) -> Union[Path, None]:
    workspace_root = find_upwards_dir(cwd, workspace_file)

    if workspace_root:
        return workspace_root

    repo_root = find_upwards_dir(cwd, root_file)

    return repo_root or find_upwards_dir(cwd, default_toml)


def get_workspace_root(cwd: Path) -> Path:
    root = find_workspace_root(cwd)

    if not root:
        raise ValueError(
            "Didn't find the workspace root. Expected to find a workspace.toml or pyproject.toml with Workspace config."
        )

    return root


def has_build_requires(pyproject: dict, value: str) -> bool:
    backend = pyproject.get("build-system", {}).get("build-backend", "")

    return value in backend


def is_poetry(pyproject: dict) -> bool:
    return has_build_requires(pyproject, "poetry")


def is_hatch(pyproject: dict) -> bool:
    return has_build_requires(pyproject, "hatchling")


def is_pdm(pyproject: dict) -> bool:
    return has_build_requires(pyproject, "pdm")


def is_pep_621_ready(pyproject: dict) -> bool:
    return pyproject.get("project", {}).get("name") is not None
