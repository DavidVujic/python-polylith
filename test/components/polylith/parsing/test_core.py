from polylith.parsing import core


expected_ns = "unittest"
bricks = {
    f"../../bases/{expected_ns}/one": f"{expected_ns}/one",
    f"../../components/{expected_ns}/two": f"{expected_ns}/two",
}


def test_parse_brick_namespace_from_path():
    res = core.parse_brick_namespace_from_path(bricks)

    assert res == expected_ns
