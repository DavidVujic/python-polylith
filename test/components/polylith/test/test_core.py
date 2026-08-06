from pathlib import Path

from polylith.test import core


def test_extract_brick_name_from_test() -> None:
    expected = "hello_world"
    root = Path.cwd()

    changed_test = root / f"test/components/my_namespace/{expected}/the_test.py"

    res = core.extract_brick_name_from_test(root, changed_test, theme="loose")

    assert res == expected
