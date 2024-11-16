from pathlib import Path

import pytest
from polylith.diff import collect

root = Path.cwd()
ns = "my_namespace"

subfolder = "python"
workspace_root_in_subfolder = Path(subfolder)

changed_files_loose = [
    Path(f"components/{ns}/a/core.py"),
    Path(f"some/other/{ns}/file.py"),
    Path(f"bases/{ns}/b/core.py"),
    Path(f"components/{ns}/b/core.py"),
    Path(f"components/{ns}/c/nested/subfolder/core.py"),
    Path(f"test/components/{ns}/x/core.py"),
    Path("projects/z/pyproject.toml"),
]

changed_files_tdd = [
    Path(f"some/other/{ns}/file.py"),
    Path(f"bases/b/src/{ns}/b/core.py"),
    Path(f"components/a/src/{ns}/a/core.py"),
    Path(f"components/b/src/{ns}/b/core.py"),
    Path(f"components/{ns}/x/core.py"),
    Path(f"components/c/src/{ns}/c/nested/subfolder/core.py"),
    Path(f"components/x/test/{ns}/x/core.py"),
    Path("projects/z/pyproject.toml"),
]


@pytest.fixture
def setup(monkeypatch):
    def set_theme(theme: str):
        monkeypatch.setattr(
            collect.configuration, "get_theme_from_config", lambda *args: theme
        )

    return set_theme


def test_get_changed_components(setup):
    setup(theme="loose")

    res = collect.get_changed_components(root, changed_files_loose, ns)

    assert res == ["a", "b", "c"]


def test_get_changed_bases(setup):
    setup(theme="loose")

    res = collect.get_changed_bases(root, changed_files_loose, ns)

    assert res == ["b"]


def test_get_changed_components_with_tdd_theme(setup):
    setup(theme="tdd")

    res = collect.get_changed_components(root, changed_files_tdd, ns)

    assert res == ["a", "b", "c"]


def test_get_changed_bases_with_tdd_theme(setup):
    setup(theme="tdd")

    res = collect.get_changed_bases(root, changed_files_tdd, ns)

    assert res == ["b"]


def test_get_changed_components_with_workspace_in_sub_folder(setup):
    setup(theme="loose")

    changes = [Path(f"{subfolder}/{p.as_posix()}") for p in changed_files_loose]

    res = collect.get_changed_components(workspace_root_in_subfolder, changes, ns)

    assert res == ["a", "b", "c"]


def test_get_changed_components_with_workspace_in_sub_folder_tdd_theme(setup):
    setup(theme="tdd")

    changes = [Path(f"{subfolder}/{p.as_posix()}") for p in changed_files_tdd]

    res = collect.get_changed_components(workspace_root_in_subfolder, changes, ns)

    assert res == ["a", "b", "c"]


def test_get_changed_projects():
    res = collect.get_changed_projects(root, changed_files_loose)

    assert res == ["z"]


def test_get_changed_projects_in_subfolder():
    changes = [Path(f"{subfolder}/{p.as_posix()}") for p in changed_files_loose]

    res = collect.get_changed_projects(workspace_root_in_subfolder, changes)

    assert res == ["z"]
