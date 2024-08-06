from pathlib import Path

from polylith import commands


def test_calculate_dependent_bricks(monkeypatch):
    fake_imports = {
        "one": {"three"},
        "two": {"three"},
        "three": {"four"},
        "four": {},
        "base_one": {"one", "four"},
        "base_two": {"two", "four"},
    }
    monkeypatch.setattr(
        commands.diff, "get_imports", lambda *args, **kwargs: fake_imports
    )

    projects_data = [
        {"bases": ["base_one", "base_two"], "components": ["one", "two", "three"]}
    ]

    changed_bricks = {"one", "three"}

    res = commands.diff.calculate_dependent_bricks(
        Path.cwd(), "test", projects_data, changed_bricks
    )

    assert res["bases"] == {"base_one"}
    assert res["components"] == {"two"}
