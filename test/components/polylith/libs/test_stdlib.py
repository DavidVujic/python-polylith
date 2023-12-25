from polylith.libs import stdlib


def test_stdlib_extras():
    py = stdlib.standard_libs["3.11"]

    assert "__future__" in py
    assert "pkg_resources" in py


def test_stdlib_3_9():
    py38 = stdlib.standard_libs["3.8"]
    py39 = stdlib.standard_libs["3.9"]

    assert py38.difference(py39) == {"_dummy_thread", "dummy_threading"}
    assert py39.difference(py38) == {"graphlib", "zoneinfo"}


def test_stdlib_3_10():
    py39 = stdlib.standard_libs["3.9"]
    py310 = stdlib.standard_libs["3.10"]

    assert py39.difference(py310) == {"formatter", "parser", "symbol"}
    assert py310.difference(py39) == {"idlelib"}


def test_stdlib_3_11():
    py310 = stdlib.standard_libs["3.10"]
    py311 = stdlib.standard_libs["3.11"]

    assert py310.difference(py311) == {"binhex"}
    assert py311.difference(py310) == {
        "tomllib",
        "_tkinter",
        "sitecustomize",
        "usercustomize",
    }


def test_stdlib_3_12():
    py311 = stdlib.standard_libs["3.11"]
    py312 = stdlib.standard_libs["3.12"]

    assert py311.difference(py312) == {
        "asynchat",
        "asyncore",
        "distutils",
        "imp",
        "smtpd",
    }
    assert py312.difference(py311) == set()
