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


def test_calculate_diff_should_identify_close_match_case_insensitive():
    brick_imports = {
        "bases": {"my_base": {}},
        "components": {
            "one": {"PIL"},
        },
    }

    third_party_libs = {"pillow"}

    res = report.calculate_diff(brick_imports, third_party_libs)

    assert len(res) == 0


def test_calculate_diff_strict_should_identify_close_match_for_dash_and_low_dash():
    brick_imports = {
        "bases": {"thebase": {"typer"}},
        "components": {
            "one": {"typing_extensions"},
        },
    }

    third_party_libs = {"typer", "typing-extensions"}

    res = report.calculate_diff(brick_imports, third_party_libs, True)

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
