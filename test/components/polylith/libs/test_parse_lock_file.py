from pathlib import Path

import pytest
from polylith.libs import lock_files

project_data = {"path": Path("./test/test_data")}

expected_libraries = {
    "annotated-types": "0.7.0",
    "anyio": "4.4.0",
    "click": "8.1.7",
    "fastapi": "0.109.2",
    "h11": "0.14.0",
    "idna": "3.7",
    "pydantic": "2.7.4",
    "pydantic-core": "2.18.4",
    "sniffio": "1.3.1",
    "starlette": "0.36.3",
    "typing-extensions": "4.12.2",
    "uvicorn": "0.25.0",
}

pdm_lock_file = "pdm"
piptools_lock_file = "piptools"
rye_lock_file = "rye"
uv_lock_file = "uv"
uv_workspace_lock_file = "uv_workspaces"

test_lock_files = {
    pdm_lock_file: "toml",
    piptools_lock_file: "text",
    rye_lock_file: "text",
    uv_lock_file: "toml",
    uv_workspace_lock_file: "toml",
}


@pytest.fixture
def setup(monkeypatch):
    monkeypatch.setattr(lock_files, "patterns", test_lock_files)


def test_find_lock_files(setup):
    res = lock_files.find_lock_files(project_data["path"])

    assert res == test_lock_files


def test_pick_lock_file(setup):
    res = lock_files.pick_lock_file(project_data["path"])

    assert res.get("filename")
    assert res.get("filetype")


def test_parse_contents_of_rye_lock_file(setup):
    names = lock_files.extract_libs(project_data, rye_lock_file, "text")

    assert names == expected_libraries


def test_parse_contents_of_pdm_lock_file(setup):
    names = lock_files.extract_libs(project_data, pdm_lock_file, "toml")

    assert names == expected_libraries


def test_parse_contents_of_pip_tools_lock_file(setup):
    names = lock_files.extract_libs(project_data, piptools_lock_file, "text")

    assert names == expected_libraries


def test_parse_contents_of_uv_lock_file(setup):
    names = lock_files.extract_libs(project_data, uv_lock_file, "toml")

    assert names == expected_libraries
