import subprocess
from pathlib import Path
from typing import List, Union

from polylith import repo, workspace


def _parse_folder_parts(folder: str, changed_file: Path) -> str:
    file_path = Path(changed_file.as_posix().replace(folder, ""))

    return next(p for p in file_path.parts if p != file_path.root)


def _get_changed(folder: str, changed_files: List[Path]) -> set:
    return {
        _parse_folder_parts(folder, f) for f in changed_files if folder in f.as_posix()
    }


def _get_changed_bricks(
    top_dir: str, changed_files: List[Path], namespace: str
) -> list:
    d = f"{top_dir}/{namespace}"

    return sorted(_get_changed(d, changed_files))


def get_changed_components(
    changed_files: List[Path], namespace: str
) -> list:
    return _get_changed_bricks(repo.components_dir, changed_files, namespace)


def get_changed_bases(changed_files: List[Path], namespace: str) -> list:
    return _get_changed_bricks(repo.bases_dir, changed_files, namespace)


def get_changed_projects(changed_files: List[Path]) -> list:
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


def get_files(tag: str) -> List[Path]:
    res = subprocess.run(
        ["git", "diff", tag, "--stat", "--name-only"],
        capture_output=True,
    )

    return [Path(p) for p in res.stdout.decode("utf-8").split()]
