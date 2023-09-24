from functools import reduce
from typing import Dict, List, Set


def _to_key_with_values(acc: Dict, alias: str) -> Dict:
    k, v = str.split(alias, "=")

    values = [str.strip(val) for val in str.split(v, ",")]

    return {**acc, **{k: values}}


def parse(aliases: List[str]) -> Dict[str, List[str]]:
    """Parse a list of aliases defined as key=value(s) into a dictionary"""
    return reduce(_to_key_with_values, aliases, {})


def pick(aliases: Dict[str, List[str]], keys: Set) -> Set:
    matrix = [v for k, v in aliases.items() if k in keys]

    flattened: List = sum(matrix, [])

    return set(flattened)
