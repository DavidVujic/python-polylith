from pathlib import Path

from poetry_polylith_plugin.components import components
from poetry_polylith_plugin.components.bases.constants import dir_name


def get_bases_data(path: Path, ns: str):
    return components.get_components_data(path, ns, dir_name)
