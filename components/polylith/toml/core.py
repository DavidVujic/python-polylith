import re
import sys
from functools import lru_cache, reduce
from pathlib import Path
from typing import List, Union

import tomlkit
from polylith import repo

if sys.version_info < (3, 11):
    import tomlkit as tomllib
else:
    import tomllib


def transform_to_package(namespace: str, include: str) -> dict:
    path, _separator, brick = str.partition(include, f"/{namespace}/")

    return {"include": f"{namespace}/{brick}", "from": path}


def get_polylith_section(data) -> dict:
    return data.get("tool", {}).get("polylith", {})


def get_custom_top_namespace_from_polylith_section(data) -> Union[str, None]:
    poly_data = get_polylith_section(data)

    return poly_data.get("build", {}).get("top-namespace")


def get_project_packages_from_polylith_section(data) -> dict:
    poly_data = get_polylith_section(data)

    bricks = poly_data.get("bricks")

    return bricks if isinstance(bricks, dict) else {}


def get_hatch_project_packages(data) -> dict:
    polylith_section = get_project_packages_from_polylith_section(data)

    if polylith_section:
        return polylith_section

    hatch_data = data["tool"]["hatch"]
    build_data = hatch_data.get("build", {}) if isinstance(hatch_data, dict) else {}

    return build_data.get("force-include", {})


def collect_configured_hatch_exclude_patterns(
    data: dict, target_name: Union[str, None]
) -> set:
    key = "exclude"

    entry = data.get("tool", {}).get("hatch", {}).get("build", {})
    targets = entry.get("targets", {})

    if target_name:
        exclude = targets.get(target_name, {}).get(key, [])
    else:
        wheel = targets.get("wheel", {}).get(key, [])
        sdist = targets.get("sdist", {}).get(key, [])
        both = entry.get(key, [])

        exclude = wheel + sdist + both

    return set(exclude)


def collect_configured_pdm_exclude_patterns(data: dict) -> set:
    entry = data.get("tool", {}).get("pdm", {}).get("build", {})
    exclude = entry.get("excludes", [])

    return set(exclude)


def collect_configured_poetry_exclude_patterns(data: dict) -> set:
    exclude = data["tool"]["poetry"].get("exclude", [])

    return set(exclude)


def collect_configured_uv_exclude_patterns(data: dict) -> set:
    entry = data.get("tool", {}).get("uv", {}).get("build-backend", {})

    wheel = entry.get("wheel-exclude", [])
    sdist = entry.get("source-exclude", [])

    exclude = wheel + sdist

    return set(exclude)


def collect_configured_exclude_patterns(
    data: dict, target_name: Union[str, None] = None
) -> set:
    if repo.is_hatch(data):
        return collect_configured_hatch_exclude_patterns(data, target_name)

    if repo.is_pdm(data):
        return collect_configured_pdm_exclude_patterns(data)

    if repo.is_poetry(data):
        return collect_configured_poetry_exclude_patterns(data)

    if repo.is_uv(data):
        return collect_configured_uv_exclude_patterns(data)

    return set()


def get_project_package_includes(namespace: str, data) -> List[dict]:
    if repo.is_poetry(data):
        return data["tool"]["poetry"].get("packages", [])

    includes = (
        get_hatch_project_packages(data)
        if repo.is_hatch(data)
        else get_project_packages_from_polylith_section(data)
    )

    return [transform_to_package(namespace, key) for key in includes.keys()]


def _remove_brick_from_mapping(mapping, brick_include: str, brick_dir_name: str) -> bool:
    try:
        items = list(mapping.items())
    except AttributeError:
        return False

    keys_to_remove = [
        k
        for k, v in items
        if v == brick_include and f"{brick_dir_name}/" in str(k).replace("\\", "/")
    ]

    for k in keys_to_remove:
        del mapping[k]

    return bool(keys_to_remove)


def _remove_brick_from_poetry_packages(
    data, brick_include: str, brick_dir_name: str
) -> bool:
    poetry = data.get("tool", {}).get("poetry")

    if not isinstance(poetry, dict):
        return False

    packages = poetry.get("packages")

    if not packages:
        return False

    indexes = [
        i
        for i, p in enumerate(list(packages))
        if p.get("include") == brick_include and brick_dir_name in str(p.get("from", ""))
    ]

    for i in reversed(indexes):
        packages.pop(i)

    if indexes and hasattr(packages, "multiline"):
        packages.multiline(True)

    return bool(indexes)


def remove_brick_from_project_packages(data, brick_include: str, brick_dir_name: str) -> bool:
    """Remove a brick from a project's packaging include configuration.

    This targets the configuration that `poly sync` updates:
    - Poetry: `[tool.poetry.packages]`
    - Hatch: `[tool.polylith.bricks]` (or `[tool.hatch.build.force-include]`)
    - PDM/PEP 621: `[tool.polylith.bricks]`

    Args:
        data: TOML document to update.
        brick_include: The include value, e.g. `my_ns/my_brick`.
        brick_dir_name: `components` or `bases`.

    Returns:
        bool: True if anything was removed.
    """

    if repo.is_poetry(data):
        return _remove_brick_from_poetry_packages(data, brick_include, brick_dir_name)

    polylith_bricks = data.get("tool", {}).get("polylith", {}).get("bricks")

    if repo.is_hatch(data):
        if polylith_bricks:
            return _remove_brick_from_mapping(
                polylith_bricks, brick_include, brick_dir_name
            )

        force_include = (
            data.get("tool", {})
            .get("hatch", {})
            .get("build", {})
            .get("force-include")
        )

        return _remove_brick_from_mapping(
            force_include, brick_include, brick_dir_name
        )

    if polylith_bricks:
        return _remove_brick_from_mapping(
            polylith_bricks, brick_include, brick_dir_name
        )

    return False


def parse_pep_621_dependency(dep: str) -> dict:
    parts = re.split(r"[\^~=!<>]", dep)

    name, *_ = parts if parts else [""]
    version = str.replace(dep, name, "")

    return {name: version} if name else {}


def parse_poetry_dependency(acc: dict, kv: tuple) -> dict:
    k, v = kv

    if isinstance(v, dict):
        extras = sorted(v.get("extras", []))
        version = v.get("version", "")

        name = k + str.replace(f"{extras}", "'", "") if extras else k
        parsed = {name: version}
    else:
        parsed = {k: v}

    return {**acc, **parsed}


def get_pep_621_optional_dependencies(data) -> List[str]:
    groups = data["project"].get("optional-dependencies", {})
    matrix = [v for v in groups.values()] if isinstance(groups, dict) else []

    return sum(matrix, [])


def is_poetry_without_pep_621_support(data) -> bool:
    return repo.is_poetry(data) and not repo.is_pep_621_ready(data)


def parse_project_dependencies(data) -> dict:
    if is_poetry_without_pep_621_support(data):
        deps = data["tool"]["poetry"].get("dependencies", {})
        res: dict = reduce(parse_poetry_dependency, deps.items(), {})

        return res

    deps = data["project"].get("dependencies", [])
    optional_deps = get_pep_621_optional_dependencies(data)

    all_deps = deps + optional_deps

    return {k: v for dep in all_deps for k, v in parse_pep_621_dependency(dep).items()}


def get_project_dependencies(data) -> dict:
    items = parse_project_dependencies(data)

    return {"items": items, "source": repo.default_toml}


def read_toml_document(path: Path) -> tomlkit.TOMLDocument:
    with path.open(encoding="utf-8", errors="ignore") as f:
        return tomlkit.loads(f.read())


@lru_cache
def load_toml(path: Path) -> dict:
    with open(path, "rb") as f:
        try:
            return tomllib.load(f)
        except tomlkit.exceptions.ParseError as e:
            raise ValueError(f"Failed loading {path}: {repr(e)}") from e
