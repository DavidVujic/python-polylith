from polylith.output import core


def test_adjust_output_return_string_without_emojis():
    data = "checking ✔ left 👈 or 👉 right"

    expected = "checking X left < or > right"

    res = core.adjust(data)

    assert res == expected
