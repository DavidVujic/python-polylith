import tomlkit
from polylith import repo
from polylith.bricks.component import create_component
from polylith.commands import delete


def test_delete_component_removes_generated_files_and_updates_pyproject(handle_workspace_files):
    root = handle_workspace_files

    options = {
        "brick": repo.components_dir,
        "namespace": "test_space",
        "package": "greet",
        "description": "test desc",
        "modulename": "core",
    }

    create_component(path=root, options=options)

    component_dir = root / "components/test_space/greet"
    test_dir = root / "test/components/test_space/greet"

    assert component_dir.exists()
    assert test_dir.exists()

    # Create a minimal hatch-style pyproject that includes the brick.
    pyproject = tomlkit.parse(
        """\
[build-system]
requires = [\"hatchling\"]
build-backend = \"hatchling.build\"

[project]
name = "development"
version = "0.0.0"

[tool.polylith.bricks]
\"components/test_space/greet\" = \"test_space/greet\"
"""
    )

    (root / repo.default_toml).write_text(tomlkit.dumps(pyproject), encoding="utf-8")

    res = delete.run(
        root,
        "test_space",
        {"brick_type": "component", "name": "greet", "dry_run": False, "force": True},
    )

    assert res is True
    assert not component_dir.exists()
    assert not test_dir.exists()

    updated = tomlkit.parse((root / repo.default_toml).read_text(encoding="utf-8"))
    bricks = updated.get("tool", {}).get("polylith", {}).get("bricks", {})

    assert "components/test_space/greet" not in bricks
