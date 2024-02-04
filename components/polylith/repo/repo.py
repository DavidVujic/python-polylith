from pathlib import Path
from typing import Union

workspace_file = "workspace.toml"
root_file = ".git"
default_toml = "pyproject.toml"
readme_file = "README.md"

bases_dir = "bases"
components_dir = "components"
projects_dir = "projects"
development_dir = "development"


def is_drive_root(cwd: Path) -> bool:
    return cwd == Path(cwd.root) or cwd == cwd.parent


def is_repo_root(cwd: Path) -> bool:
    fullpath = cwd / root_file

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
    workspace_root = find_upwards_dir(cwd, workspace_file)
    if workspace_root:
        return workspace_root
    return find_upwards_dir(cwd, root_file)


def get_workspace_root(cwd: Path) -> Path:
    root = find_workspace_root(cwd)

    if not root:
        raise ValueError(
            "Didn't find the workspace root. Expected to find a workspace.toml or .git file."
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
    if is_poetry(pyproject):
        return False

    return pyproject.get("project", {}).get("name") is not None
