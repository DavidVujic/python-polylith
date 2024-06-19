import tomlkit


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

    with open("./test/test_data/requirements.lock", "r") as f:
        data = f.readlines()

    rows = (str.strip(line) for line in data)
    filtered = (row for row in rows if row and not row.startswith(("#", "-")))
    parts = (str.split(row, "==") for row in filtered)
    names = {row[0] for row in parts}

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

    with open("./test/test_data/pdm.lock", "r") as f:
        data = tomlkit.load(f)

    names = {p.get("name") for p in data.get("package", [])}

    assert names == expected
