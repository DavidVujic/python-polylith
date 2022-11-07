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
