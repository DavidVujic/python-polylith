from polylith.distributions import collect


def test_parse_third_party_library_name():
    fake_project_deps = {
        "items": {
            "python": "^3.10",
            "fastapi": "^0.110.0",
            "uvicorn[standard]": "^0.27.1",
            "python-jose[cryptography]": "^3.3.0",
            "hello[world, something]": "^3.3.0",
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


def test_collect_known_aliases_and_sub_dependencies():
    fake_deps = {
        "items": {"typer": "1", "hello-world-library": "2"},
        "source": "unit-test",
    }

    fake_alias = ["hello-world-library=hello"]

    res = collect.known_aliases_and_sub_dependencies(fake_deps, fake_alias, {})

    assert "typer" in res
    assert "typing-extensions" in res
    assert "hello" in res
