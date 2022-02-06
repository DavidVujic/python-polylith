from pathlib import Path
from poetry_polylith_plugin.components.files import create_file


keep_file_name = ".keep"


def create_dir(path: Path, dir_name: str, keep=False) -> Path:
    d = path / dir_name
    d.mkdir(parents=True)

    if keep:
        create_file(d, keep_file_name)

    return d
