from polylith.deps.core import (
    calculate_brick_deps,
    find_bricks_with_circular_dependencies,
)


def test_calculate_brick_deps() -> None:
    bricks = {"bases": {"base"}, "components": {"one", "two", "three", "four"}}

    imports = {
        "base": {"base", "one"},
        "one": {"one", "four"},
        "two": {"two"},
        "three": {"three", "one"},
        "four": {"four", "two"},
    }

    res = calculate_brick_deps("one", bricks, imports)

    assert sorted(res["used_by"]) == ["base", "three"]
    assert sorted(res["uses"]) == ["four"]


def test_find_bricks_with_circular_dependencies() -> None:
    deps = {
        "base": {"used_by": [], "uses": ["one", "four"]},
        "one": {"used_by": ["two", "three"], "uses": ["three"]},
        "two": {"used_by": "three", "uses": []},
        "three": {"used_by": ["one"], "uses": ["one", "two"]},
        "four": {"used_by": ["base"], "uses": ["two"]},
    }

    res = find_bricks_with_circular_dependencies(deps)

    assert res == {"one": {"three"}, "three": {"one"}}
