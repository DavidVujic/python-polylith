import re
import subprocess
from pathlib import Path
from typing import List, Set, Union

from polylith import configuration, repo


def _parse_folder_parts(pattern: str, changed_file: Path) -> str:
    parts = re.split(pattern, changed_file.as_posix())
    remainder = parts[-1]

    file_path = Path(remainder)

    return next(p for p in file_path.parts if p != file_path.root)


def _get_changed(pattern: str, changed_files: List[Path]) -> set:
    return {
        _parse_folder_parts(pattern, f)
        for f in changed_files
        if re.match(pattern, f.as_posix())
    }


def _parse_path_pattern(root: Path, top_dir: str, namespace: str) -> str:
    theme = configuration.get_theme_from_config(root)

    if theme == "loose":
        return f"{top_dir}/{namespace}/"

    return rf"({top_dir}\/).+(\/src\/)({namespace})"


def _get_changed_bricks(
    root: Path, top_dir: str, changed_files: List[Path], namespace: str
) -> list:
    pattern = _parse_path_pattern(root, top_dir, namespace)

    return sorted(_get_changed(pattern, changed_files))


def get_changed_components(
    root: Path, changed_files: List[Path], namespace: str
) -> list:
    return _get_changed_bricks(root, repo.components_dir, changed_files, namespace)


def get_changed_bases(root: Path, changed_files: List[Path], namespace: str) -> list:
    return _get_changed_bricks(root, repo.bases_dir, changed_files, namespace)


def get_changed_projects(changed_files: List[Path]) -> list:
    res = _get_changed(repo.projects_dir, changed_files)
    filtered = {p for p in res if p != repo.projects_dir}
    return sorted(filtered)


def get_latest_tag(root: Path, key: Union[str, None]) -> Union[str, None]:
    tag_pattern = configuration.get_tag_pattern_from_config(root, key)
    sorting_options = [
        f"--sort={option}"
        for option in configuration.get_tag_sort_options_from_config(root)
    ]

    res = subprocess.run(
        ["git", "tag", "-l"] + sorting_options + [f"{tag_pattern}"],
        capture_output=True,
    )

    return next((tag for tag in res.stdout.decode("utf-8").split()), None)


def get_files(tag: str) -> List[Path]:
    res = subprocess.run(
        ["git", "diff", tag, "--stat", "--name-only"],
        capture_output=True,
    )

    return [Path(p) for p in res.stdout.decode("utf-8").split()]


def _affected(projects_data: List[dict], brick_type: str, bricks: List[str]) -> set:
    res = {
        p["path"].name: set(p.get(brick_type, [])).intersection(bricks)
        for p in projects_data
    }

    return {k for k, v in res.items() if v}


def get_projects_affected_by_changes(
    projects_data: List[dict],
    projects: List[str],
    bases: List[str],
    components: List[str],
) -> Set[str]:
    a = _affected(projects_data, "components", components)
    b = _affected(projects_data, "bases", bases)
    c = set(projects)

    return {*a, *b, *c}
