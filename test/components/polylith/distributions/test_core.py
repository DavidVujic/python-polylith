import importlib.metadata

from polylith import distributions


def test_distribution_packages():
    dists = list(importlib.metadata.distributions())

    res = distributions.distributions_packages(dists)

    expected_dist = "mypy-extensions"
    expected_package = "mypy_extensions"

    assert res.get(expected_dist) is not None
    assert res[expected_dist] == [expected_package]


def test_parse_package_name_from_dist_requires():
    assert "greenlet" == distributions.core.only_package_name("greenlet !=0.4.17")
    assert "mysqlclient" == distributions.core.only_package_name(
        "mysqlclient >=1.4.0 ; extra == 'mysql'"
    )
    assert "typing-extensions" == distributions.core.only_package_name(
        "typing-extensions>=4.6.0)"
    )
    assert "pymysql" == distributions.core.only_package_name(
        "pymysql ; extra == 'pymysql'"
    )
