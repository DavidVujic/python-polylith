from functools import lru_cache
from pathlib import Path

import yaml


@lru_cache
def load_yaml(path: Path) -> dict:
    with open(path, "rb") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Failed loading {path}: {repr(e)}") from e
