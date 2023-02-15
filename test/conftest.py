import shutil
from pathlib import Path

import pytest


@pytest.fixture(scope="function")
def handle_workspace_files():
    temp_dir = Path("test/temp")
    temp_dir.mkdir(parents=True, exist_ok=True)
    workspace_file = temp_dir / "workspace.toml"
    workspace_file.touch()
    source_file = Path("test/test_data/workspace.toml")
    workspace_file.write_text(source_file.read_text())
    yield temp_dir
    shutil.rmtree(temp_dir)
