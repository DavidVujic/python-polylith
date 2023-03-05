from typing import Set, Union


def only_brick_imports(imports: Set[str], top_ns: str) -> Set[str]:
    return {i for i in imports if i.startswith(top_ns)}


def only_bricks(import_data: dict, top_ns: str) -> dict:
    return {k: only_brick_imports(v, top_ns) for k, v in import_data.items()}


def brick_import_to_name(brick_import: str) -> Union[str, None]:
    parts = brick_import.split(".")

    return parts[1] if len(parts) > 1 else None


def only_brick_name(brick_imports: Set[str]) -> Set:
    res = {brick_import_to_name(i) for i in brick_imports}

    return {i for i in res if i}


def only_brick_names(import_data: dict) -> dict:
    return {k: only_brick_name(v) for k, v in import_data.items() if v}


def exclude_empty(import_data: dict) -> dict:
    return {k: v for k, v in import_data.items() if v}


def extract_brick_imports(all_imports: dict, top_ns) -> dict:
    with_only_bricks = only_bricks(all_imports, top_ns)
    with_only_brick_names = only_brick_names(with_only_bricks)

    return exclude_empty(with_only_brick_names)
