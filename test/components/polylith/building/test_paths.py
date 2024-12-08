from pathlib import Path

import pytest
import tomlkit
from polylith.building import paths

toml_data = """\
[tool.polylith.bricks]
"../../components/my_namespace/my_brick" = "my_namespace/my_brick"
"""

top_ns_toml_data = """\
[tool.polylith.build]
top-namespace = "helloworld"

[tool.polylith.bricks]
"../../components/my_namespace/my_brick" = "my_namespace/my_brick"
"""

toml_data_without_bricks = """\
[tool.polylith.bricks]
"""

toml_data_with_other_includes = """\
[tool.polylith.bricks]
"" = ""
"""


@pytest.mark.parametrize(
    "config, expected",
    [
        (toml_data, Path("my_namespace")),
        (top_ns_toml_data, Path("helloworld")),
        (toml_data_without_bricks, None),
        (toml_data_with_other_includes, None),
    ],
)
def test_calculate_destination_dir(config, expected):
    data = tomlkit.loads(config)

    res = paths.calculate_destination_dir(data)

    assert res == expected
