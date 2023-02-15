from test import params

import pytest

from components.polylith.bricks.base import create_base, get_bases_data


@pytest.mark.parametrize(
    "id, expected_dirs, expected_dir_structure",
    params.create_base_params,
    ids=params.create_base_ids,
)
def test_create_base(handle_workspace_files, id, expected_dirs, expected_dir_structure):

    create_base(
        path=handle_workspace_files,
        namespace="test_namespace",
        package="test_package",
        description="test desc",
    )
    results = [
        x for x in handle_workspace_files.iterdir() if x.name != "workspace.toml"
    ]

    assert handle_workspace_files.is_dir()
    assert all([item.is_dir() for item in results if item in expected_dirs])
    assert (
        set([item.name for item in results]).intersection(expected_dirs)
        == expected_dirs
    )
    assert all([item.exists for item in expected_dir_structure])


def test_get_bases_data_valid_with_test_file_structure(create_test_base):

    result = get_bases_data(create_test_base, "test_namespace")
    assert result == [{"name": "test_package"}]
