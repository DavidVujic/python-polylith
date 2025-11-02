import tomlkit
from polylith import toml

namespace = "unittest"

poetry_toml = """\
[tool.poetry]
packages = [
    {include = "unittest/one",from = "../../bases"},
    {include = "unittest/two",from = "../../components"}
]
exclude = ["**/one/*"]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

hatch_toml = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.force-include]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

hatch_toml_alternative = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build]
something = "something"

[tool.polylith.bricks]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

hatch_toml_combined = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.force-include]
"something" = "else"

[tool.polylith.bricks]
"../../bases/unittest/one" = "unittest/one"
"../../components/unittest/two" = "unittest/two"
"""

pep_621_toml_deps = """\
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
dependencies = ["fastapi~=0.109.2", "uvicorn~=0.25.0", "tomlkit"]

[project.optional-dependencies]
dev = ["an-optional-lib==1.2.3", "another"]
local = ["awsglue-local-dev==1.0.0"]
"""

poetry_toml_deps = """\
[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.110.0"
uvicorn = {extras = ["standard"], version = "^0.27.1"}
tomlkit = "*"

an-optional-lib = {version = "1.2.3", optional = true}
another = {optional = true}
awsglue-local-dev = {version = "1.0.0", optional = true}

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
"""

uv_toml = """\
[build-system]
requires = ["uv_build>=0.9.6,<0.10.0"]
build-backend = "uv_build"
"""

pdm_toml = """\
[build-system]
requires = ["pdm-backend"]
build-backend = "pdm.backend"

[tool.pdm.build]
excludes = ["**/one/*"]
"""

expected_packages = [
    {"include": "unittest/one", "from": "../../bases"},
    {"include": "unittest/two", "from": "../../components"},
]


def test_get_poetry_package_includes():
    data = tomlkit.loads(poetry_toml)

    res = toml.get_project_package_includes(namespace, data)

    assert res == expected_packages


def test_get_hatch_package_includes():
    data = tomlkit.loads(hatch_toml)

    res = toml.get_project_package_includes(namespace, data)

    assert res == expected_packages


def test_get_hatch_package_includes_in_build_hook():
    data = tomlkit.loads(hatch_toml_alternative)

    res = toml.get_project_package_includes(namespace, data)

    assert res == expected_packages


def test_get_hatch_package_includes_from_default_when_in_both():
    data = tomlkit.loads(hatch_toml_combined)

    res = toml.get_project_package_includes(namespace, data)

    assert res == expected_packages


def test_parse_pep_621_project_dependencies():
    expected_dependencies = {
        "fastapi": "~=0.109.2",
        "uvicorn": "~=0.25.0",
        "tomlkit": "",
        "an-optional-lib": "==1.2.3",
        "another": "",
        "awsglue-local-dev": "==1.0.0",
    }

    data = tomlkit.loads(pep_621_toml_deps)

    res = toml.parse_project_dependencies(data)

    assert res == expected_dependencies


def test_parse_poetry_project_dependencies():
    expected_dependencies = {
        "python": "^3.10",
        "fastapi": "^0.110.0",
        "uvicorn[standard]": "^0.27.1",
        "tomlkit": "*",
        "an-optional-lib": "1.2.3",
        "another": "",
        "awsglue-local-dev": "1.0.0",
    }

    data = tomlkit.loads(poetry_toml_deps)

    res = toml.parse_project_dependencies(data)

    assert res == expected_dependencies


def test_collect_hatch_exclude_patterns() -> None:
    build_data = """\
[tool.hatch.build]
exclude = ["**/one/*"]
"""

    data = tomlkit.loads(hatch_toml + build_data)
    assert toml.collect_configured_exclude_patterns(data, None) == {"**/one/*"}


def test_collect_hatch_wheel_exclude_patterns() -> None:
    build_data = """\
[tool.hatch.build.targets.wheel]
exclude = ["**/two/*"]
"""

    data = tomlkit.loads(hatch_toml + build_data)
    assert toml.collect_configured_exclude_patterns(data, None) == {"**/two/*"}


def test_collect_hatch_sdist_exclude_patterns() -> None:
    build_data = """\
[tool.hatch.build.targets.sdist]
exclude = ["**/two/*"]
"""

    data = tomlkit.loads(hatch_toml + build_data)
    assert toml.collect_configured_exclude_patterns(data, None) == {"**/two/*"}


def test_collect_hatch_wheel_and_sdist_exclude_patterns() -> None:
    build_data = """\
[tool.hatch.build]
exclude = ["**/one/*"]

[tool.hatch.build.targets.wheel]
exclude = ["**/two/*"]

[tool.hatch.build.targets.sdist]
exclude = ["**/three/*"]
"""

    data = tomlkit.loads(hatch_toml + build_data)
    assert toml.collect_configured_exclude_patterns(data, None) == {
        "**/one/*",
        "**/two/*",
        "**/three/*",
    }
    assert toml.collect_configured_exclude_patterns(data, "wheel") == {"**/two/*"}
    assert toml.collect_configured_exclude_patterns(data, "sdist") == {"**/three/*"}


def test_collect_pdm_exclude_patterns() -> None:
    data = tomlkit.loads(pdm_toml)
    assert toml.collect_configured_exclude_patterns(data, None) == {"**/one/*"}


def test_collect_poetry_exclude_patterns() -> None:
    data = tomlkit.loads(poetry_toml)
    assert toml.collect_configured_exclude_patterns(data, None) == {"**/one/*"}


def test_collect_uv_combined_exclude_patterns() -> None:
    build_data = """\
[tool.uv.build-backend]
source-exclude = ["**/one/*"]
wheel-exclude = ["**/two/*"]
"""
    data = tomlkit.loads(uv_toml + build_data)
    assert toml.collect_configured_exclude_patterns(data, None) == {
        "**/one/*",
        "**/two/*",
    }
