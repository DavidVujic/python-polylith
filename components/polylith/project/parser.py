from pathlib import Path
from typing import List


def to_path(package: dict) -> Path:
    include = package["include"]
    from_path = package.get("from")

    return Path(f"{from_path}/{include}") if from_path else Path(include)


def parse_package_paths(packages: List[dict]) -> List[Path]:
    sorted_packages = sorted(packages, key=lambda p: (p.get("from", "."), p["include"]))

    return [to_path(p) for p in sorted_packages]
