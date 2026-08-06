from pathlib import Path

from polylith.test import core


def test_extract_brick_name_from_test() -> None:
    expected = "hello_world"
    root = Path.cwd()

    first_test = root / f"test/components/my_namespace/{expected}/the_test.py"
    second_test = root / f"components/{expected}/my_namespace/{expected}/test/the_test.py"

    first = core.extract_brick_name_from_test(root, first_test, theme="loose")
    second = core.extract_brick_name_from_test(root, second_test, theme="tdd")

    assert first == expected
    assert second == expected


def test_extract_brick_type_from_test() -> None:
    root = Path.cwd()

    loose_base_test = root / "test/bases/my_namespace/hello/the_test.py"
    loose_comp_test = root / "test/components/my_namespace/world/the_test.py"

    tdd_base_test = root / "bases/hello/my_namespace/hello/test/the_test.py"
    tdd_comp_test = root / "components/world/my_namespace/world/test/the_test.py"

    first = core.extract_brick_type_from_test(root, loose_base_test, theme="loose")
    second = core.extract_brick_type_from_test(root, loose_comp_test, theme="loose")

    third = core.extract_brick_type_from_test(root, tdd_base_test, theme="tdd")
    fourth = core.extract_brick_type_from_test(root, tdd_comp_test, theme="tdd")

    assert first == "bases"
    assert second == "components"

    assert third == "bases"
    assert fourth == "components"
