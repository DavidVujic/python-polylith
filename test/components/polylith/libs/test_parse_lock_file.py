from pathlib import Path

from polylith.libs import lock_files

project_data = {"path": Path("./test/test_data")}

expected_libraries = {
    "annotated-types",
    "anyio",
    "click",
    "fastapi",
    "h11",
    "idna",
    "pydantic",
    "pydantic-core",
    "sniffio",
    "starlette",
    "typing-extensions",
    "uvicorn",
}


def test_find_lock_file():
    expected = {
        "pdm.lock": "toml",
        "requirements.lock": "text",
        "requirements.txt": "text",
    }

    res = lock_files.find_lock_file(project_data)

    assert res == expected


def test_parse_contents_of_rye_lock_file():
    names = lock_files.extract_lib_names(project_data, {"requirements.lock": "text"})

    assert names == expected_libraries


def test_parse_contents_of_pdm_lock_file():
    expected = {*expected_libraries, *{"colorama", "exceptiongroup"}}

    names = lock_files.extract_lib_names(project_data, {"pdm.lock": "toml"})

    assert names == expected


def test_parse_contents_of_pip_tools_lock_file():
    names = lock_files.extract_lib_names(project_data, {"requirements.txt": "text"})

    assert names == expected_libraries
