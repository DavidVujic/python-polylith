from polylith.commands import check


def test_collect_known_aliases_and_sub_dependencies():
    fake_project_data = {
        "deps": {"items": {"typer", "hello-world-library"}, "source": "unit-test"}
    }
    fake_options = {"alias": ["hello-world-library=hello"]}

    res = check.collect_known_aliases(fake_project_data, fake_options)

    assert "typer" in res
    assert "typing-extensions" in res
    assert "hello" in res
