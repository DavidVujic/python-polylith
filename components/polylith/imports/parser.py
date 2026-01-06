import ast
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import FrozenSet, List, Set, Union

typing_ns = "typing"
type_checking = "TYPE_CHECKING"


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


def find_type_checking_body(node: ast.If) -> List[ast.stmt]:
    if isinstance(node.test, ast.Name) and node.test.id == type_checking:
        return node.body

    if isinstance(node.test, ast.Attribute) and node.test.attr == type_checking:
        if isinstance(node.test.value, ast.Name) and node.test.value.id == typing_ns:
            return node.body

    return []


def flatten(data: Iterable) -> list:
    return [item for nested in data for item in nested]


def parse_node(node: ast.AST) -> Union[dict, None]:
    if isinstance(node, ast.Import):
        return {"include": parse_import(node)}

    if isinstance(node, ast.ImportFrom):
        return {"include": parse_import_from(node)}

    if isinstance(node, ast.If):
        found = find_type_checking_body(node)
        parsed = flatten(parse_imports(f) for f in found)

        if not parsed:
            return None

        return {"exclude": parsed}

    return None


def find_imported(node_id: str, imported: FrozenSet[str]) -> Union[str, None]:
    return next((i for i in imported if str.endswith(i, f".{node_id}")), None)


def extract_api_part(path: str) -> str:
    *_parts, api = str.split(path, ".")

    return api


def find_matching_node(expr: ast.expr, imported: FrozenSet[str]) -> Union[str, None]:
    api = {extract_api_part(i) for i in imported}

    if isinstance(expr, ast.Name) and expr.id in api:
        return find_imported(expr.id, imported)

    return None


def parse_import_usage(node: ast.AST, imported: FrozenSet[str]) -> Union[str, None]:
    found = None
    child = None

    wrapper_nodes = (ast.Await, ast.Expr, ast.NamedExpr, ast.Starred, ast.Subscript)

    if isinstance(node, ast.Attribute):
        found = find_matching_node(node.value, imported)
        child = node.value
    elif isinstance(node, wrapper_nodes):
        child = node.value
    elif isinstance(node, ast.Call):
        found = find_matching_node(node.func, imported)
        child = node.func
    elif isinstance(node, ast.UnaryOp):
        child = node.operand

    if found:
        return found

    return parse_import_usage(child, imported) if child is not None else None


def parse_module(path: Path) -> ast.AST:
    with open(path.as_posix(), "r", encoding="utf-8", errors="ignore") as f:
        tree = ast.parse(f.read(), path.name)

    return tree


@lru_cache(maxsize=None)
def extract_imports(path: Path) -> List[str]:
    tree = parse_module(path)

    nodes = (parse_node(n) for n in ast.walk(tree))
    parsed_nodes = [n for n in nodes if n is not None]

    includes = [i for n in parsed_nodes for i in n.get("include", [])]
    excludes = {i for n in parsed_nodes for i in n.get("exclude", [])}

    return [i for i in includes if i not in excludes]


def extract_and_flatten(py_modules: Iterable) -> Set[str]:
    return {i for m in py_modules for i in extract_imports(m)}


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


def fetch_import_usages_in_module(path: Path, imported: FrozenSet[str]) -> Set[str]:
    tree = parse_module(path)

    nodes = (parse_import_usage(n, imported) for n in ast.walk(tree))

    return {n for n in nodes if n is not None}


@lru_cache(maxsize=None)
def fetch_brick_import_usages(path: Path, imported: FrozenSet[str]) -> Set[str]:
    py_modules = find_files(path)

    res = (fetch_import_usages_in_module(p, imported) for p in py_modules)

    return {i for n in res if n for i in n}


def extract_api(paths: Set[str]) -> Set[str]:
    return {extract_api_part(p) for p in paths}


def fetch_api(paths: Set[Path]) -> dict:
    interfaces = [Path(p / "__init__.py") for p in paths]

    rows = [{i.parent.name: extract_api(list_imports(i))} for i in interfaces]

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
