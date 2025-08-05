_cache = {}


def add(key: str, value) -> None:
    _cache[key] = value


def get(key: str):
    return _cache[key]


def exists(key: str) -> bool:
    return key in _cache


def clear() -> None:
    _cache.clear()
