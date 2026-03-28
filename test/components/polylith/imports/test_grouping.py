from polylith.imports import (
    extract_brick_imports,
    extract_brick_imports_with_namespaces,
)

top_ns = "my_ns"

all_imports = {
    "brick_a": {"hello.world", f"{top_ns}.first", "typing.Set"},
    "brick_b": {"httpx.Request"},
    "brick_c": {f"{top_ns}.second"},
    "brick_d": {top_ns},
}


def test_extract_brick_imports() -> None:
    res = extract_brick_imports(all_imports, top_ns)

    assert res == {
        "brick_a": {"first"},
        "brick_c": {"second"},
    }


def test_extract_brick_imports_when_third_party_starts_with_top_ns() -> None:
    extra = {"brick_x": {f"{top_ns}_something_else.Request"}}

    combined = {**all_imports, **extra}
    res = extract_brick_imports(combined, top_ns)

    assert res == {
        "brick_a": {"first"},
        "brick_c": {"second"},
    }


def test_extract_brick_imports_with_ns() -> None:
    res = extract_brick_imports_with_namespaces(all_imports, top_ns)

    assert res == {
        "brick_a": {f"{top_ns}.first"},
        "brick_c": {f"{top_ns}.second"},
        "brick_d": {top_ns},
    }


def test_extract_brick_imports_with_ns_when_third_party_starts_with_top_ns() -> None:
    extra = {"brick_x": {f"{top_ns}_something_else.Request"}}

    combined = {**all_imports, **extra}
    res = extract_brick_imports_with_namespaces(combined, top_ns)

    assert res == {
        "brick_a": {f"{top_ns}.first"},
        "brick_c": {f"{top_ns}.second"},
        "brick_d": {top_ns},
    }
