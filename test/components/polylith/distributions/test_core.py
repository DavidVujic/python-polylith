import importlib.metadata
import sys

from polylith import distributions


def test_distribution_packages():
    dists = list(importlib.metadata.distributions())

    res = distributions.distributions_packages(dists)

    expected_dist = "mypy-extensions"
    expected_package = "mypy_extensions"

    assert res.get(expected_dist) is not None
    assert res[expected_dist] == [expected_package]


def test_parse_package_name_from_dist_requires():
    expected = {
        "greenlet": "greenlet !=0.4.17",
        "mysqlclient": "mysqlclient >=1.4.0 ; extra == 'mysql'",
        "typing-extensions": "typing-extensions>=4.6.0",
        "pymysql": "pymysql ; extra == 'pymysql'",
        "one": "one<=0.4.17",
        "two": "two^=0.4.17",
        "three": "three~=0.4.17",
    }

    for k, v in expected.items():
        assert k == distributions.core.parse_sub_package_name(v)


def test_distribution_sub_packages():
    dists = list(importlib.metadata.distributions())

    res = distributions.distributions_sub_packages(dists)

    expected_dist = "typer"
    expected_sub_package = "typing-extensions"

    assert res.get(expected_dist) is not None
    assert expected_sub_package in res[expected_dist]


def test_package_distributions_returning_top_namespace(monkeypatch):
    fake_dists = {
        "something": ["something-subnamespace"],
        "opentelemetry": ["opentelemetry-instrumentation-fastapi"],
        "google": ["google-cloud-storage", "google-api-core"],
        "other": ["other-sub-ns"],
    }

    fake_project_deps = {
        "opentelemetry-instrumentation-fastapi",
        "fastapi",
        "something-subnamespace",
        "google-cloud-storage",
    }

    if sys.version_info > (3, 9):
        monkeypatch.setattr(
            distributions.core.importlib.metadata,
            "packages_distributions",
            lambda: fake_dists,
        )

    res = distributions.core.get_packages_distributions(fake_project_deps)

    assert res == {"google", "opentelemetry", "something"}
