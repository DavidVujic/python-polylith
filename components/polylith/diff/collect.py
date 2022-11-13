import subprocess
from pathlib import Path
from typing import Union

from polylith import repo, workspace


def _get_changed(folder: str, changed_files: list[Path]) -> set:
    return {p.parent.name for p in changed_files if folder in p.as_posix()}


def _get_changed_bricks(root: Path, top_dir: str, changed_files: list[Path]) -> list:
    namespace = workspace.parser.get_namespace_from_config(root)
    d = f"{top_dir}/{namespace}"

    return sorted(_get_changed(d, changed_files))


def get_changed_components(root: Path, changed_files: list[Path]) -> list:
    return _get_changed_bricks(root, repo.components_dir, changed_files)


def get_changed_bases(root: Path, changed_files: list[Path]) -> list:
    return _get_changed_bricks(root, repo.bases_dir, changed_files)


def get_changed_projects(changed_files: list[Path]) -> list:
    res = _get_changed(repo.projects_dir, changed_files)
    filtered = {p for p in res if p != repo.projects_dir}
    return sorted(filtered)


def get_latest_tag(root: Path) -> Union[str, None]:
    tag_pattern = workspace.parser.get_git_tag_pattern_from_config(root)

    res = subprocess.run(
        ["git", "tag", "-l", "--sort=-committerdate", f"{tag_pattern}"],
        capture_output=True,
    )

    return next((tag for tag in res.stdout.decode("utf-8").split()), None)


def get_files(tag: str) -> list[Path]:
    res = subprocess.run(
        ["git", "diff", tag, "--stat", "--name-only"],
        capture_output=True,
    )

    return [Path(p) for p in res.stdout.decode("utf-8").split()]
