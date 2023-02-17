import shutil
from pathlib import Path

import pytest
from polylith.bricks.base import create_base


@pytest.fixture(scope="function")
def handle_workspace_files():
    """Creates a temporary directory with a valid workspace file and removes the directory in tear-down.

    Yields:
        Path: The temp directory path
    """
    temp_dir = Path("test/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    workspace_file = temp_dir / "workspace.toml"
    workspace_file.touch()
    source_file = Path("test/test_data/workspace.toml")
    workspace_file.write_text(source_file.read_text())
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="function")
def create_test_base(handle_workspace_files):
    """Uses the temp directory and creates bases for testing.

    Args:
        handle_workspace_files (fixture): Sets up the needed temp directory.

    Yields:
        Path: The temp directory path, to be passed to the function under test.

    Note:
        The handle_workspace_files fixture will clean up at tear-down.
    """
    create_base(
        path=handle_workspace_files,
        namespace="test_namespace",
        package="test_package",
        description="test desc",
    )
    yield handle_workspace_files
