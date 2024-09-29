from pathlib import Path

import pytest
from polylith.libs import lock_files

test_path = Path("./test/test_data")
project_data = {"path": test_path}

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


def test_parse_contents_of_uv_workspaces_aware_lock_file(setup):
    expected_gcp_libs = {
        "functions-framework": "3.5.0",
        "click": "8.1.7",
        "colorama": "0.4.6",
        "cloudevents": "1.11.0",
        "deprecation": "2.1.0",
        "packaging": "24.1",
        "flask": "3.0.3",
        "blinker": "1.8.2",
        "importlib-metadata": "8.2.0",
        "zipp": "3.20.0",
        "itsdangerous": "2.2.0",
        "jinja2": "3.1.4",
        "markupsafe": "2.1.5",
        "werkzeug": "3.0.3",
        "gunicorn": "23.0.0",
        "watchdog": "4.0.2",
    }

    expected_consumer_libs = {"confluent-kafka": "2.3.0"}

    lock_file_format = "toml"

    gcp_libs = lock_files.extract_workspace_member_libs(
        test_path,
        project_data | {"name": "my-gcp-function-project"},
        uv_workspace_lock_file,
        lock_file_format,
    )

    consumer_libs = lock_files.extract_workspace_member_libs(
        test_path,
        project_data | {"name": "consumer-project"},
        uv_workspace_lock_file,
        lock_file_format,
    )

    aws_lambda_libs = lock_files.extract_workspace_member_libs(
        test_path,
        project_data | {"name": "my-aws-lambda-project"},
        uv_workspace_lock_file,
        lock_file_format,
    )

    assert gcp_libs == expected_gcp_libs
    assert consumer_libs == expected_consumer_libs
    assert aws_lambda_libs == {}
