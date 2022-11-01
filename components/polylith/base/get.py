from pathlib import Path

from polylith.component import get
from polylith.base.constants import dir_name


def get_bases_data(path: Path, ns: str) -> list[dict]:
    return get.get_components_data(path, ns, dir_name)
