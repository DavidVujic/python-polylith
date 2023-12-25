"""
Using the dependencies of the development virtual environment
to assert the Poetry internals itself,
and catch any breaking features in upcoming versions.
"""

from pathlib import Path

from poetry.factory import Factory
from polylith.poetry import internals


def test_find_third_party_libs():
    path = Path.cwd()

    dev_poetry = Factory().create_poetry(path)

    res = internals.find_third_party_libs(dev_poetry, path)

    expected = {"rich", "isort", "black"}

    assert expected.issubset(res)


def test_distributions():
    path = Path.cwd()

    dev_poetry = Factory().create_poetry(path)

    res = internals.distributions(dev_poetry, path)

    assert res is not None and len(list(res))


def test_distribution_packages():
    path = Path.cwd()

    dev_poetry = Factory().create_poetry(path)
    dists = internals.distributions(dev_poetry, path)

    res = internals.distributions_packages(dists)

    expected_dist = "mypy-extensions"
    expected_package = "mypy_extensions"

    assert res.get(expected_dist) is not None
    assert res[expected_dist] == [expected_package]
