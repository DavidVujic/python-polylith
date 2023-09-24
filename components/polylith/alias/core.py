from functools import reduce
from typing import List, Set


def _to_key_with_values(acc: dict, alias: str) -> dict:
    k, v = str.split(alias, "=")

    values = [str.strip(val) for val in str.split(v, ",")]

    return {**acc, **{k: values}}


def parse(aliases: list[str]) -> dict[str, List[str]]:
    """Parse a list of aliases defined as key=value(s) into a dictionary"""
    return reduce(_to_key_with_values, aliases, {})


def pick(aliases: dict[str, List[str]], keys: Set) -> Set:
    matrix = [v for k, v in aliases.items() if k in keys]

    flattened: List = sum(matrix, [])

    return set(flattened)
