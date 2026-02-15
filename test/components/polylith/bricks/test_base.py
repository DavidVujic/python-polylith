from pathlib import Path

from polylith.bricks.base import create_base, get_bases_data


def test_create_base(handle_workspace_files, tmp_path: Path):
    options = {
        "namespace": "test_namespace",
        "package": "test_package",
        "description": "test desc",
        "modulename": "core",
    }
    create_base(path=handle_workspace_files, options=options)

    expected_dirs = [
        Path(tmp_path / "bases/test_namespace/test_package/core.py"),
        Path(tmp_path / "test/bases/test_namespace/test_package/test_core.py"),
    ]

    assert all(item.exists() for item in expected_dirs)


def test_get_bases_data_valid_with_test_file_structure(create_test_base):
    result = get_bases_data(create_test_base, "test_namespace")
    assert result == [{"name": "test_package"}]
