from pathlib import Path


def to_path(package: dict) -> Path:
    include = package["include"]
    from_path = package.get("from")

    return Path(f"{from_path}/{include}") if from_path else Path(include)


def parse_package_paths(packages: list[dict]) -> list[Path]:
    sorted_packages = sorted(packages, key=lambda p: (p["from"], p["include"]))

    return [to_path(p) for p in sorted_packages]
