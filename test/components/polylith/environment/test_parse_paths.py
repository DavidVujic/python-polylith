from pathlib import Path

import tomlkit
from polylith.environment import parse_paths

root = "/some/path"
namespace = "my_namespace"

toml_with_tdd_theme = f"""\
[tool.polylith.bricks]
"bases/one/src/{namespace}/one" = "{namespace}/one"
"components/two/src/{namespace}/two" = "{namespace}/two"

[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"
"""


def test_parse_paths_for_loose_theme():
    res = parse_paths(Path(root), "loose", namespace, {})

    assert res == {f"{root}/bases", f"{root}/components"}


def test_parse_paths_for_tdd_theme():
    data = tomlkit.loads(toml_with_tdd_theme)

    res = parse_paths(Path(root), "tdd", namespace, data)

    assert res == {f"{root}/bases/one/src", f"{root}/components/two/src"}
