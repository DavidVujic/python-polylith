from polylith.commands import sync


def test_can_run_interactive_mode_depending_on_the_quite_mode() -> None:
    project_data = {"type": "project", "bases": [], "components": []}
    with_bricks = {"type": "project", "bases": [], "components": ["one", "two"]}

    assert sync.can_run_interactive_mode(project_data, {"quiet": False}) is True

    assert sync.can_run_interactive_mode(project_data, {"quiet": True}) is False
    assert sync.can_run_interactive_mode(with_bricks, {"quiet": True}) is False


def test_can_run_interactive_mode_returns_false_for_project_with_bricks() -> None:
    options = {"quiet": False}
    with_bases = {"type": "project", "bases": ["my_base"], "components": []}
    with_components = {"type": "project", "bases": [], "components": ["one", "two"]}

    assert sync.can_run_interactive_mode(with_bases, options) is False
    assert sync.can_run_interactive_mode(with_components, options) is False
