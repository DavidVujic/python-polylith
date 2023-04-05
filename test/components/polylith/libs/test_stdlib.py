from polylith.libs import stdlib


def test_stdlib_3_9() -> None:
    py38 = stdlib.standard_libs["3.8"]
    py39 = stdlib.standard_libs["3.9"]

    assert py38.difference(py39) == {"_dummy_thread", "dummy_threading"}
    assert py39.difference(py38) == {"graphlib", "zoneinfo"}


def test_stdlib_3_10() -> None:
    py39 = stdlib.standard_libs["3.9"]
    py310 = stdlib.standard_libs["3.10"]

    assert py39.difference(py310) == {"formatter", "parser", "symbol"}
    assert py310.difference(py39) == {"idlelib"}


def test_stdlib_3_11() -> None:
    py310 = stdlib.standard_libs["3.10"]
    py311 = stdlib.standard_libs["3.11"]

    assert py310.difference(py311) == {"binhex"}
    assert py311.difference(py310) == {"tomllib"}
