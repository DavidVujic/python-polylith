import importlib.metadata

from polylith import distributions


def test_distribution_packages():
    dists = importlib.metadata.distributions()

    res = distributions.distributions_packages(dists)

    expected_dist = "mypy-extensions"
    expected_package = "mypy_extensions"

    assert res.get(expected_dist) is not None
    assert res[expected_dist] == [expected_package]
