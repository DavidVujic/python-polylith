import ast
from functools import lru_cache
from pathlib import Path
from typing import Optional, Set

from polylith.imports import SYMBOLS, extract_api, list_imports, parse_module


def target_names(t: ast.AST) -> Set[str]:
    if isinstance(t, ast.Name):
        return {t.id}

    if isinstance(t, (ast.Tuple, ast.List)):
        return {n for e in t.elts for n in target_names(e)}

    return set()


def extract_variables(statement: ast.stmt) -> Set[str]:
    if isinstance(statement, ast.Assign):
        return {n for t in statement.targets for n in target_names(t)}

    if isinstance(statement, (ast.AnnAssign, ast.AugAssign)):
        return target_names(statement.target)

    if hasattr(ast, "TypeAlias") and isinstance(statement, ast.TypeAlias):
        return {statement.name.id}

    return set()


def is_private(symbol_name: str) -> bool:
    return symbol_name.startswith("_")


@lru_cache(maxsize=None)
def parse(path: Path) -> ast.Module:
    return parse_module(path)


def extract_symbols(path: Path) -> Set[str]:
    tree = parse(path)

    return {
        s.name for s in tree.body if isinstance(s, SYMBOLS) and not is_private(s.name)
    }


def extract_public_variables(path: Path) -> Set[str]:
    tree = parse(path)

    return {v for s in tree.body for v in extract_variables(s) if not is_private(v)}


def is_the_all_statement(target: ast.expr) -> bool:
    return isinstance(target, ast.Name) and target.id == "__all__"


def is_string_constant(expression: ast.AST) -> bool:
    return isinstance(expression, ast.Constant) and isinstance(expression.value, str)


def find_the_all_variable(statement: ast.stmt) -> Optional[Set[str]]:
    if not isinstance(statement, ast.Assign):
        return None

    if not any(is_the_all_statement(t) for t in statement.targets):
        return None

    if not isinstance(statement.value, (ast.List, ast.Tuple)):
        return None

    if not all(is_string_constant(e) for e in statement.value.elts):
        return None

    return {e.value for e in statement.value.elts if isinstance(e, ast.Constant)}


def extract_the_all_variable(path: Path) -> Set[str]:
    tree = parse(path)

    res = [find_the_all_variable(s) for s in tree.body]

    return next((r for r in res if r is not None), set())


def extract_imported_api(path: Path) -> Set[str]:
    return extract_api(list_imports(path))


def fetch_api_for_path(path: Path) -> Set[str]:
    imported_api = extract_imported_api(path)
    symbols = extract_symbols(path)
    variables = extract_public_variables(path)
    the_all_variable = extract_the_all_variable(path)

    return imported_api | symbols | variables | the_all_variable


def fetch_api(paths: Set[Path]) -> dict:
    interfaces = [Path(p / "__init__.py") for p in paths]

    rows = [{i.parent.name: fetch_api_for_path(i)} for i in interfaces]

    return {k: v for row in rows for k, v in row.items()}
