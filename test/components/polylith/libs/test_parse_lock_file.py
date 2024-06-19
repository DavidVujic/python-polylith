from pathlib import Path

from polylith.libs import lock_files

project_data = {"path": Path("./test/test_data")}


def test_find_lock_file():
    expected = {
        "pdm.lock": "toml",
        "requirements.lock": "text",
    }

    res = lock_files.find_lock_file(project_data)

    assert res == expected


def test_parse_contents_of_rye_lock_file():
    expected = {
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

    names = lock_files.extract_lib_names(project_data, {"requirements.lock": "text"})

    assert names == expected


def test_parse_contents_of_pdm_lock_file():
    expected = {
        "annotated-types",
        "anyio",
        "click",
        "colorama",
        "exceptiongroup",
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

    names = lock_files.extract_lib_names(project_data, {"pdm.lock": "toml"})

    assert names == expected
