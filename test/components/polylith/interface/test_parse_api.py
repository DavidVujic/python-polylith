import ast
import io
from functools import partial
from pathlib import Path

from polylith.interface import parser

fake_path = Path.cwd()


the_interface = """
THE_DATA = {"a": "b"}

_the_private_var = "should not extract this one"


class Hello:
    pass


def helloworld():
    pass


def goodbye():
    pass

__all__ = ["thing", "other", "message"]
"""

extracted_imports = {"a.b.c", "d.e.f"}


def fake_parse(contents: str, *args, **kwargs) -> ast.AST:
    f = io.StringIO(contents)

    return ast.parse(f.read(), "unit_test")


def test_extract_api(monkeypatch) -> None:
    monkeypatch.setattr(parser, "list_imports", lambda *args: extracted_imports)

    res = parser.extract_imported_api(fake_path)

    assert res == {"c", "f"}


def test_extract_symbols(monkeypatch) -> None:
    fn = partial(fake_parse, the_interface)
    monkeypatch.setattr(parser, "parse", fn)

    res = parser.extract_symbols(fake_path)

    assert res == {"Hello", "helloworld", "goodbye"}


def test_extract_variables(monkeypatch) -> None:
    fn = partial(fake_parse, the_interface)
    monkeypatch.setattr(parser, "parse", fn)

    res = parser.extract_public_variables(fake_path)

    assert res == {"THE_DATA"}


def test_extract_the_all_variable(monkeypatch) -> None:
    fn = partial(fake_parse, the_interface)
    monkeypatch.setattr(parser, "parse", fn)

    res = parser.extract_the_all_variable(fake_path)

    assert res == {"thing", "other", "message"}


def test_extract_the_all_variable_from_module_pointer(tmp_path: Path) -> None:
    expected = "pub_func"

    parser.parse.cache_clear()

    package_dir = tmp_path / "comp"
    package_dir.mkdir(parents=True)

    init = package_dir / "__init__.py"
    core = package_dir / "core.py"

    init.write_text(
        """
from .core import *\


__all__ = core.__all__
"""
    )

    core.write_text(
        f"""
__all__ = ["{expected}"]


def pub_func():
    pass
"""
    )

    assert parser.extract_the_all_variable(init) == {expected}
    assert parser.fetch_api_for_path(init) == {expected}


def test_fetch_api_for_path(monkeypatch) -> None:
    fn = partial(fake_parse, the_interface)

    monkeypatch.setattr(parser, "parse", fn)
    monkeypatch.setattr(parser, "list_imports", lambda *args: extracted_imports)

    res = parser.fetch_api_for_path(fake_path)

    assert res == {
        "c",
        "f",
        "Hello",
        "helloworld",
        "goodbye",
        "THE_DATA",
        "thing",
        "other",
        "message",
    }
