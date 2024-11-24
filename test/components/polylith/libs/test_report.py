import pytest
from polylith.libs import report

third_party_libs = {
    "cleo",
    "mypy-extensions",
    "poetry",
    "tomlkit",
    "requests",
    "rich",
}


def test_calculate_diff_reports_no_diff():
    brick_imports = {
        "bases": {"my_base": {"rich"}},
        "components": {
            "one": {"rich"},
            "two": {"rich", "cleo"},
            "thre": {"tomlkit"},
        },
    }

    res = report.calculate_diff(brick_imports, third_party_libs)

    assert len(res) == 0


def test_calculate_diff_should_report_missing_dependency():
    expected_missing = "aws-lambda-powertools"

    brick_imports = {
        "bases": {"my_base": {"poetry"}},
        "components": {
            "one": {"tomlkit"},
            "two": {"tomlkit", expected_missing, "rich"},
            "three": {"rich"},
        },
    }

    res = report.calculate_diff(brick_imports, third_party_libs)

    assert res == {expected_missing}


@pytest.mark.parametrize(
    "imports, is_strict",
    [
        ({"aws_lambda_powertools", "PIL", "pyyoutube"}, False),
        ({"typing_extensions"}, True),
    ],
)
def test_calculate_diff_should_identify_close_match(imports: set, is_strict: bool):
    brick_imports = {
        "bases": {"thebase": {"typer"}},
        "components": {"one": imports},
    }

    libs = {
        "aws-lambda-powertools",
        "pillow",
        "python-youtube",
        "typer",
        "typing-extensions",
    }

    res = report.calculate_diff(brick_imports, libs, is_strict)

    assert len(res) == 0


def test_libs_versions_diff():
    dev_data = {"deps": {"items": {"rich": "13.*"}}}
    projects_data = [{"name": "one", "deps": {"items": {"rich": "13.*"}}}]

    assert report.libs_with_different_versions(dev_data, projects_data) == set()


def test_libs_versions_diff_should_return_libs_with_different_versions():
    dev_data = {"deps": {"items": {"rich": "13.*"}}}

    proj_one = {"name": "one", "deps": {"items": {"rich": "13.*"}}}
    proj_two = {"name": "two", "deps": {"items": {"rich": "11.*"}}}
    projects_data = [proj_one, proj_two]

    res = report.libs_with_different_versions(dev_data, projects_data)

    assert res == {"rich"}


def test_libs_versions_diff_should_only_return_libs_with_different_versions():
    dev_data = {"deps": {"items": {"rich": "13.*"}}}

    proj_one = {"name": "one", "deps": {"items": {"rich": "13.*"}}}
    proj_two = {"name": "two", "deps": {"items": {}}}

    projects_data = [proj_one, proj_two]

    res = report.libs_with_different_versions(dev_data, projects_data)

    assert res == set()
