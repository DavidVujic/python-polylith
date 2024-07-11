from polylith.distributions import collect


def test_parse_third_party_library_name():
    fake_project_deps = {
        "items": {
            "python": "^3.10",
            "fastapi": "^0.110.0",
            "uvicorn[standard]": "^0.27.1",
            "python-jose[cryptography]": "^3.3.0",
            "hello[world, something]": "^3.3.0"
        },
        "source": "pyproject.toml",
    }

    expected = {
        "python",
        "fastapi",
        "uvicorn",
        "standard",
        "python-jose",
        "cryptography",
        "hello",
        "world",
        "something",
    }

    res = collect.extract_library_names(fake_project_deps)

    assert res == expected
