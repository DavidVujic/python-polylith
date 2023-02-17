from pathlib import Path

import pytest
from polylith.bricks.base import create_base, get_bases_data

create_base_params = [
    (
        "1. Creates expected directories and files",
        set(["bases", "test"]),
        set(
            [
                Path("test/temp/bases/test_namespace/test_package/core.py"),
                Path("test/temp/test/bases/test_namespace/test_package/test_core.py"),
            ]
        ),
    )
]
create_base_ids = [x[0] for x in create_base_params]


@pytest.mark.parametrize(
    "id, expected_dirs, expected_dir_structure",
    create_base_params,
    ids=create_base_ids,
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

    assert all([item.is_dir() for item in results if item in expected_dirs])
    assert (
        set([item.name for item in results]).intersection(expected_dirs)
        == expected_dirs
    )
    assert all([item.exists for item in expected_dir_structure])


def test_get_bases_data_valid_with_test_file_structure(create_test_base):

    result = get_bases_data(create_test_base, "test_namespace")
    assert result == [{"name": "test_package"}]
