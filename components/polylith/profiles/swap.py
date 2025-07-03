import importlib
import os
import sys
from collections.abc import Sequence
from importlib.machinery import ModuleSpec, PathFinder
from types import ModuleType
from typing import Union


class SwappableBricks(PathFinder):
    @classmethod
    def find_spec(
        cls,
        fullname: str,
        path: Union[Sequence[str], None] = None,
        target: Union[ModuleType, None] = None,
    ) -> Union[ModuleSpec, None]:
        swap_from = "todo"
        swap_to = "todo_v2"

        if not fullname.endswith(swap_from):
            return None

        sys.modules[fullname] = importlib.import_module(swap_to)

        return super().find_spec(swap_to, path, target)


def by_profile():
    if os.getenv("PROFILE") != "todo":
        return

    sys.meta_path.insert(0, SwappableBricks)


"""
in a sitecustomize.py

from polylith.profiles import swap

swap.by_profile()

"""
