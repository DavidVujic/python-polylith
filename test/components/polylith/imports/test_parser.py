import ast
import io
from functools import partial
from pathlib import Path

from polylith.imports import usages

fake_path = Path.cwd()


top_ns = "top_namespace"
brick = "something"
imported = {f"{top_ns}.{brick}"}


ns_brick_import = f"""
from {top_ns} import {brick}


def first() -> str:
    return {brick}.one()


def second() -> str:
    return {brick}.two()
"""

ns_brick_fn_import = f"""
from {top_ns}.{brick} import one, two


def first() -> str:
    return one()


def second() -> str:
    return two()
"""


ns_brick_import_with_shadowed = f"""
from {top_ns} import {brick}


def second({brick}: dict) -> str:
    return {brick}.get("key")
"""

ns_import = f"""
import {top_ns}


def first() -> str:
    return {top_ns}.x.one()


def second() -> str:
    return {top_ns}.{brick}.one()

"""

ns_import_star = f"""
from {top_ns} import *


def first() -> str:
    return x.one()


def second() -> str:
    return {brick}.one()

"""


def fake_parse_module(contents: str, *args, **kwargs) -> ast.AST:
    f = io.StringIO(contents)

    return ast.parse(f.read(), "unit_test")


def test_fetch_import_usages_in_module_ns_brick(monkeypatch) -> None:
    fn = partial(fake_parse_module, ns_brick_import)
    monkeypatch.setattr(usages, "parse_module", fn)

    expected = {f"{top_ns}.{brick}.one", f"{top_ns}.{brick}.two"}

    res = usages.fetch_import_usages_in_module(fake_path, top_ns, imported)

    assert res == expected


def test_fetch_import_usages_in_module_ns_brick_fn(monkeypatch) -> None:
    fn = partial(fake_parse_module, ns_brick_import)
    monkeypatch.setattr(usages, "parse_module", fn)

    expected = {f"{top_ns}.{brick}.one", f"{top_ns}.{brick}.two"}

    res = usages.fetch_import_usages_in_module(fake_path, top_ns, imported)

    assert res == expected


def test_fetch_import_usages_in_module_ns_brick_with_shadowed(monkeypatch) -> None:
    fn = partial(fake_parse_module, ns_brick_import_with_shadowed)
    monkeypatch.setattr(usages, "parse_module", fn)

    res = usages.fetch_import_usages_in_module(fake_path, top_ns, imported)

    assert res == set()


def test_fetch_import_usages_in_module_ns(monkeypatch) -> None:
    fn = partial(fake_parse_module, ns_import)
    monkeypatch.setattr(usages, "parse_module", fn)

    expected = {f"{top_ns}.{brick}.one"}

    res = usages.fetch_import_usages_in_module(fake_path, top_ns, imported)

    assert res == expected


def test_fetch_import_usages_in_module_ns_star(monkeypatch) -> None:
    fn = partial(fake_parse_module, ns_import_star)
    monkeypatch.setattr(usages, "parse_module", fn)

    expected = {f"{top_ns}.{brick}.one"}

    res = usages.fetch_import_usages_in_module(fake_path, top_ns, imported)

    assert res == expected
