import importlib.metadata
import sys
from typing import Union

import pytest
from polylith import distributions


@pytest.fixture
def reset():
    distributions.core.parsed_namespaces_from_files.cache_clear()


class FakeDist:
    def __init__(
        self,
        name: str,
        read_text_data: Union[str, None] = None,
    ):
        self.read_text_data = read_text_data
        self.metadata = {"name": name}

    def read_text(self, *args):
        return self.read_text_data


def test_distribution_packages(reset):
    dists = list(importlib.metadata.distributions())

    res = distributions.distributions_packages(dists)

    expected_dist = "mypy-extensions"
    expected_package = "mypy_extensions"

    assert res.get(expected_dist) is not None
    assert res[expected_dist] == [expected_package]


def test_distribution_packages_parse_contents_of_top_level_txt(reset):
    dists = [FakeDist("python-jose", "jose\njose/backends\n")]

    res = distributions.distributions_packages(dists)

    expected_dist = "python-jose"
    expected_packages = ["jose", "jose.backends"]

    assert res.get(expected_dist) is not None
    assert res[expected_dist] == expected_packages


def test_distribution_packages_with_no_top_level_ns_information(reset, monkeypatch):
    monkeypatch.setattr(
        distributions.core.importlib.metadata, "files", lambda name: None
    )

    dists = [FakeDist("some_package")]

    res = distributions.distributions_packages(dists)

    assert res == {}


def test_distribution_packages_with_top_level_ns_information_in_files(
    reset, monkeypatch
):
    files = [
        importlib.metadata.PackagePath("some_module.py"),
        importlib.metadata.PackagePath("hello/world.py"),
        importlib.metadata.PackagePath("some_package/some_module.py"),
        importlib.metadata.PackagePath("something/else.sh"),
    ]

    monkeypatch.setattr(
        distributions.core.importlib.metadata, "files", lambda name: files
    )

    dists = [FakeDist("some_package")]

    res = distributions.distributions_packages(dists)

    assert res == {"some_package": ["hello"]}


def test_parse_package_name_from_dist_requires(reset):
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


def test_distribution_sub_packages(reset):
    dists = list(importlib.metadata.distributions())

    res = distributions.distributions_sub_packages(dists)

    expected_dist = "typer"
    expected_sub_package = "typing-extensions"

    assert res.get(expected_dist) is not None
    assert expected_sub_package in res[expected_dist]


@pytest.mark.skipif(sys.version_info < (3, 10), reason="requires python3.10 or higher")
def test_package_distributions_returning_top_namespace(reset, monkeypatch):
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

    monkeypatch.setattr(
        distributions.core.importlib.metadata,
        "packages_distributions",
        lambda: fake_dists,
    )

    res = distributions.core.get_packages_distributions(fake_project_deps)

    assert res == {"google", "opentelemetry", "something"}


@pytest.mark.skipif(sys.version_info > (3, 9), reason="asserting python3.9 and lower")
def test_package_distributions_returning_empty_set(reset):
    fake_project_deps = {"something-subnamespace"}

    res = distributions.core.get_packages_distributions(fake_project_deps)

    assert res == set()
