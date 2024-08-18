"""
Using the dependencies of the development virtual environment
to assert the Poetry internals itself,
and catch any breaking features in upcoming versions.
"""

from pathlib import Path

from polylith.poetry import internals


def test_find_third_party_libs():
    path = Path.cwd()
    res = internals.find_third_party_libs(path)

    expected = {"rich", "isort", "black"}

    assert expected.issubset(res)


def test_distributions():
    path = Path.cwd()

    res = internals.distributions(path)

    assert res is not None and len(list(res))
