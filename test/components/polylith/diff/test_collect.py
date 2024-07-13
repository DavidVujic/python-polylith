from polylith.diff import collect
from pathlib import Path
import pytest

root = Path.cwd()
ns = "my_namespace"


changed_files_loose = [
    Path(f"components/{ns}/a/core.py"),
    Path(f"some/other/{ns}/file.py"),
    Path(f"bases/{ns}/b/core.py"),
    Path(f"components/{ns}/b/core.py"),
    Path(f"components/{ns}/c/nested/subfolder/core.py"),
]

changed_files_tdd = [
    Path(f"some/other/{ns}/file.py"),
    Path(f"bases/b/src/{ns}/b/core.py"),
    Path(f"components/a/src/{ns}/a/core.py"),
    Path(f"components/b/src/{ns}/b/core.py"),
    Path(f"components/{ns}/x/core.py"),
    Path(f"components/c/src/{ns}/c/nested/subfolder/core.py"),
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
