from polylith.libs import report


def test_calculate_diff_reports_no_diff():
    brick_imports = {
        "bases": {"my_base": {"rich"}},
        "components": {
            "one": {"rich"},
            "two": {"rich", "cleo"},
            "thre": {"tomlkit"},
        },
    }

    third_party_libs = {
        "tomlkit",
        "cleo",
        "requests",
        "rich",
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

    third_party_libs = {
        "tomlkit",
        "poetry",
        "mypy-extensions",
        "rich",
    }

    res = report.calculate_diff(brick_imports, third_party_libs)

    assert res == {expected_missing}


def test_calculate_diff_should_identify_close_match():
    brick_imports = {
        "bases": {"my_base": {"poetry"}},
        "components": {
            "one": {"tomlkit"},
            "two": {"tomlkit", "aws_lambda_powertools", "rich"},
            "three": {"rich", "pyyoutube"},
        },
    }

    third_party_libs = {
        "tomlkit",
        "python-youtube",
        "poetry",
        "aws-lambda-powertools",
        "rich",
    }

    res = report.calculate_diff(brick_imports, third_party_libs)

    assert len(res) == 0
