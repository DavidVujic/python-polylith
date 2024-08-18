from pathlib import Path

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


def pick_lock_file(project_data: dict) -> dict:
    data = find_lock_files(project_data["path"])
    first = next(iter(data.items()), None)

    if not first:
        return {}

    filename, filetype = first

    return {"filename": filename, "filetype": filetype}


def extract_lib_names_from_toml(path: Path) -> dict:
    data = load_toml(path)

    return {p["name"]: p["version"] for p in data.get("package", [])}


def parse_name(row: str) -> str:
    parts = str.split(row, "==")

    return parts[0]


def parse_version(row: str) -> str:
    parts = str.split(row, "==")[1]
    res = str.split(parts, " ")

    return res[0]


def extract_lib_names_from_txt(path: Path) -> dict:
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
            return extract_lib_names_from_toml(path)

        return extract_lib_names_from_txt(path)
    except (IndexError, KeyError, ValueError) as e:
        raise ValueError(f"Failed reading {filename}: {repr(e)}") from e
