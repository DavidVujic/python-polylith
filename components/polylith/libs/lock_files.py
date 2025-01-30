from functools import reduce
from pathlib import Path
from typing import List

from polylith.toml import load_toml

patterns = {
    "pdm.lock": "toml",
    "poetry.lock": "toml",
    "uv.lock": "toml",
    "requirements.lock": "text",
    "requirements.txt": "text",
}


def find_lock_files(path: Path) -> dict:
    return {k: v for k, v in patterns.items() if Path(path / k).exists()}


def pick_lock_file(path: Path) -> dict:
    data = find_lock_files(path)
    first = next(iter(data.items()), None)

    if not first:
        return {}

    filename, filetype = first

    return {"filename": filename, "filetype": filetype}


def extract_libs_from_packages(packages: List[dict]) -> dict:
    return {p["name"]: p["version"] for p in packages}


def extract_libs_from_toml(path: Path) -> dict:
    data = load_toml(path)

    return extract_libs_from_packages(data.get("package", []))


def parse_name(row: str) -> str:
    parts = str.split(row, "==")

    return parts[0]


def parse_version(row: str) -> str:
    parts = str.split(row, "==")[1]
    res = str.split(parts, " ")

    return res[0]


def extract_libs_from_txt(path: Path) -> dict:
    with open(path, "r") as f:
        data = f.readlines()

    rows = (str.strip(line) for line in data)
    filtered = (row for row in rows if row and not row.startswith(("#", "-")))

    return {parse_name(row): parse_version(row) for row in filtered}


def extract_libs(project_data: dict, filename: str, filetype: str) -> dict:
    dir_path = project_data["path"]

    path = Path(dir_path / filename)

    if not path.exists():
        return {}

    try:
        if filetype == "toml":
            return extract_libs_from_toml(path)

        return extract_libs_from_txt(path)
    except (IndexError, KeyError, ValueError) as e:
        raise ValueError(f"Failed reading {filename}: {repr(e)}") from e


def is_from_lock_file(deps: dict) -> bool:
    return any(deps["source"] == s for s in set(patterns.keys()))


def get_workspace_members(data: dict) -> List[str]:
    return data.get("manifest", {}).get("members", [])


def get_workspace_enabled_lock_file_data(
    root: Path, filename: str, filetype: str
) -> dict:
    if filetype != "toml":
        return {}

    path = Path(root / filename)

    if not path.exists():
        return {}

    data = load_toml(path)
    members = get_workspace_members(data)

    return data if members else {}


def pick_package_sub_deps(package: dict) -> list:
    package_sub_deps = package.get("dependencies", [])

    package_optional_deps_section = package.get("optional-dependencies", {})
    package_optional_deps: List[dict] = sum(package_optional_deps_section.values(), [])

    return package_sub_deps + package_optional_deps


def pick_packages(data: dict, name: str) -> list:
    package = next(p for p in data["package"] if p["name"] == name)

    package_sub_deps = pick_package_sub_deps(package)
    nested_package_deps = [pick_packages(data, p["name"]) for p in package_sub_deps]

    flattened = sum(nested_package_deps, [])

    return [package] + flattened if flattened else [package]


def normalized(name: str) -> str:
    chars = {"_", "."}

    normalized = reduce(lambda acc, char: str.replace(acc, char, "-"), chars, name)

    return str.lower(normalized)


def extract_workspace_member_libs(data: dict, project_data: dict) -> dict:
    members = get_workspace_members(data)
    member_name = normalized(project_data["name"])

    if member_name not in members:
        return {}

    try:
        packages = pick_packages(data, member_name)
        extracted = extract_libs_from_packages(packages)
    except KeyError as e:
        raise ValueError(f"Failed parsing lock-file data: {repr(e)}") from e

    return {k: v for k, v in extracted.items() if k != member_name}
