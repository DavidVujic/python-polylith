from pathlib import Path

from polylith.component import get
from polylith.repo import bases_dir


def get_bases_data(path: Path, ns: str) -> list[dict]:
    return get.get_components_data(path, ns, bases_dir)
