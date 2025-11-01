import ast
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import List, Set


def parse_import(node: ast.Import) -> List[str]:
    return [name.name for name in node.names]


def extract_import_from(node: ast.ImportFrom) -> List:
    return (
        [f"{node.module}.{alias.name}" for alias in node.names]
        if node.names
        else [node.module]
    )


def parse_import_from(node: ast.ImportFrom) -> List[str]:
    return extract_import_from(node) if node.module and node.level == 0 else []


def parse_imports(node: ast.AST) -> List[str]:
    if isinstance(node, ast.Import):
        return parse_import(node)

    if isinstance(node, ast.ImportFrom):
        return parse_import_from(node)

    return []


def parse_module(path: Path) -> ast.AST:
    with open(path.as_posix(), "r", encoding="utf-8", errors="ignore") as f:
        tree = ast.parse(f.read(), path.name)

    return tree


def extract_imports(path: Path) -> List[str]:
    tree = parse_module(path)

    return [i for node in ast.walk(tree) for i in parse_imports(node) if i is not None]


def extract_and_flatten(py_modules: Iterable) -> Set[str]:
    extracted = (extract_imports(m) for m in py_modules)
    flattened = (i for imports in extracted for i in imports)

    return set(flattened)


def is_python_file(path: Path) -> bool:
    return path.is_file() and path.suffix == ".py"


def find_files(path: Path) -> Iterable:
    return [path] if is_python_file(path) else path.rglob("*.py")


@lru_cache(maxsize=None)
def list_imports(path: Path) -> Set[str]:
    py_modules = find_files(path)

    return extract_and_flatten(py_modules)


def fetch_all_imports(paths: Set[Path]) -> dict:
    rows = [{p.name: list_imports(p)} for p in paths]

    return {k: v for row in rows for k, v in row.items()}


def should_exclude(path: Path, excludes: Set[str]):
    return any(path.match(pattern) for pattern in excludes)


def list_excluded_imports(path: Path, excludes: Set[str]) -> Set[str]:
    py_modules = find_files(path)

    filtered = [p for p in py_modules if should_exclude(p, excludes)]

    return extract_and_flatten(filtered)


def fetch_excluded_imports(paths: Set[Path], excludes: Set[str]) -> dict:
    rows = [{p.name: list_excluded_imports(p, excludes)} for p in paths]

    return {k: v for row in rows for k, v in row.items()}


def extract_top_ns_from_imports(imports: Set[str]) -> Set:
    return {imp.split(".")[0] for imp in imports}


def extract_top_ns(import_data: dict) -> dict:
    return {k: extract_top_ns_from_imports(v) for k, v in import_data.items()}
