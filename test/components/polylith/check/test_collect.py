from polylith.check import collect

brick_imports = {
    "bases": {"base_one": {"base_one", "component_one"}},
    "components": {
        "component_one": {"component_one", "component_two", "component_tree"},
        "component_two": {"component_two"},
        "component_three": {"component_three"},
    },
}

bases = {"base_one"}


def test_find_unused_bricks_returns_no_unused_bricks():
    components = {"component_one", "component_two", "component_tree"}

    res = collect.find_unused_bricks(brick_imports, bases, components)

    assert res == set()


def test_find_unused_bricks_returns_unused_bricks():
    expected = {"component_four"}
    components = set().union({"component_one", "component_two"}, expected)

    res = collect.find_unused_bricks(brick_imports, bases, components)

    assert res == expected
