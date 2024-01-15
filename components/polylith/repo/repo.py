from pathlib import Path
from typing import Union

workspace_file = "workspace.toml"
default_toml = "pyproject.toml"
readme_file = "README.md"

bases_dir = "bases"
components_dir = "components"
projects_dir = "projects"
development_dir = "development"


def is_drive_root(cwd: Path) -> bool:
    return cwd == Path(cwd.root) or cwd == cwd.parent


def is_repo_root(cwd: Path) -> bool:
    fullpath = cwd / ".git"

    return fullpath.exists()


def find_upwards(cwd: Path, name: str) -> Union[Path, None]:
    if is_drive_root(cwd):
        return None

    fullpath = cwd / name

    if fullpath.exists():
        return fullpath

    if is_repo_root(cwd):
        return None

    return find_upwards(cwd.parent, name)


def find_upwards_dir(cwd: Path, name: str) -> Union[Path, None]:
    fullpath = find_upwards(cwd, name)

    return fullpath.parent if fullpath else None


def find_workspace_root(cwd: Path) -> Union[Path, None]:
    return find_upwards_dir(cwd, workspace_file)


def get_workspace_root(cwd: Path) -> Path:
    root = find_workspace_root(cwd)

    if not root:
        raise ValueError(
            "Didn't find the workspace root. Expected to find a workspace.toml file."
        )

    return root


def is_poetry(pyproject: dict) -> bool:
    return pyproject.get("tool", {}).get("poetry") is not None


def is_hatch(pyproject: dict) -> bool:
    return pyproject.get("tool", {}).get("hatch") is not None


def is_pep_621_ready(pyproject: dict) -> bool:
    if is_poetry(pyproject):
        return False

    return pyproject.get("project", {}).get("name") is not None
