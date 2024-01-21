from polylith.hatch import core


def test_parse_namespace():
    expected = "unittest"

    bricks = {
        f"../../bases/{expected}/one": f"{expected}/one",
        f"../../components/{expected}/two": f"{expected}/two",
    }

    assert core.parse_namespace(bricks) == expected
