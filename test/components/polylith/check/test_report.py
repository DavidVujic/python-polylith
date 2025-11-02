from polylith.check import report


def test_extract_collected_imports() -> None:
    ns = "my_top_namespace"

    imports_in_bases = {
        "cli": {
            f"{ns}.first.thing",
            f"{ns}.second.thing",
            "tomlkit",
        }
    }

    imports_in_components = {
        "first": {
            f"{ns}.third",
        },
        "second": {
            "functools.reduce",
            "httpx",
            "io.StringIO",
            "pathlib.Path",
        },
        "third": {},
    }

    expected = {
        "brick_imports": {
            "bases": {"cli": {"first", "second"}},
            "components": {"first": {"third"}},
        },
        "third_party_imports": {
            "bases": {"cli": {"tomlkit"}},
            "components": {"second": {"httpx"}},
        },
    }

    res = report.extract_collected_imports(ns, imports_in_bases, imports_in_components)

    assert res == expected
