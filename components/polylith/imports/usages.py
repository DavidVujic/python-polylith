import ast
from functools import lru_cache
from pathlib import Path
from typing import FrozenSet, Set, Tuple, Union

from polylith.imports.parser import extract_imports, find_files, parse_module

WRAPPER_NODES = (ast.Await, ast.Expr, ast.NamedExpr, ast.Starred, ast.Subscript)
FN_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
SYMBOLS = (*FN_NODES, ast.ClassDef)


def extract_api_part(path: str) -> str:
    return path.rsplit(".", 1)[-1]


def extract_api(paths: Set[str]) -> Set[str]:
    return {extract_api_part(p) for p in paths}


def find_import_root_and_path(
    expr: ast.expr, parts: Tuple[str, ...] = ()
) -> Tuple[ast.expr, str]:
    """Builds a namespace when the expression is an Attribute or Name, otherwise empty."""
    if isinstance(expr, ast.Attribute):
        return find_import_root_and_path(expr.value, (*parts, expr.attr))

    namespace_parts = (*parts, expr.id) if isinstance(expr, ast.Name) else parts

    namespace = str.join(".", reversed(namespace_parts))

    return expr, namespace


def with_ns(usage: str, ns: str) -> str:
    return usage if str.startswith(usage, ns + ".") else f"{ns}.{usage}"


def match_usage(root_id: str, usage: str, entry: str) -> str:
    separator = "."

    part, *rest = str.split(usage, separator)

    if root_id == usage:
        return entry

    if root_id == part:
        return f"{separator}".join([entry, *rest])

    return usage


def find_matching_usage(expr: ast.expr, options: dict) -> Union[str, None]:
    ns = options["ns"]
    api_map = options["api_map"]
    allowed_prefixes = options["allowed_prefixes"]
    shadowed = options["shadowed"]

    root, usage = find_import_root_and_path(expr)

    if not isinstance(root, ast.Name):
        return None

    if root.id in shadowed:
        return None

    if root.id in api_map:
        entry = api_map[root.id]
        found = match_usage(root.id, usage, entry)

        return with_ns(found, ns)

    if any(usage.startswith(p + ".") for p in allowed_prefixes):
        return with_ns(usage, ns)

    return None


def parse_import_usage(node: ast.AST, options: dict) -> Union[str, None]:
    usage = None
    child = None

    if isinstance(node, ast.Attribute):
        usage = find_matching_usage(node, options)
        child = node.value
    elif isinstance(node, WRAPPER_NODES):
        child = node.value
    elif isinstance(node, ast.Call):
        usage = find_matching_usage(node.func, options)
        child = node.func
    elif isinstance(node, ast.UnaryOp):
        child = node.operand

    if usage:
        return usage

    return parse_import_usage(child, options) if child is not None else None


def collect_arg_names(
    fn: Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda],
) -> Set[str]:
    args = fn.args

    names = {a.arg for a in args.posonlyargs + args.args + args.kwonlyargs}

    if args.vararg:
        names.add(args.vararg.arg)

    if args.kwarg:
        names.add(args.kwarg.arg)

    return names


def walk_usages(node: ast.AST, options: dict) -> Set[str]:
    if isinstance(node, FN_NODES):
        options = {
            **options,
            "shadowed": options["shadowed"] | frozenset(collect_arg_names(node)),
        }

    out = set()
    hit = parse_import_usage(node, options)

    if hit:
        out.add(hit)

    for child in ast.iter_child_nodes(node):
        out |= walk_usages(child, options)

    return out


def fetch_import_usages_in_module(path: Path, ns: str, imported: Set[str]) -> Set[str]:
    tree = parse_module(path)
    api_map = {extract_api_part(p): p for p in imported}

    options = {
        "ns": ns,
        "api_map": api_map,
        "allowed_prefixes": frozenset(api_map.values()),
        "shadowed": frozenset(),
    }
    return walk_usages(tree, options)


@lru_cache(maxsize=None)
def fetch_brick_import_usages(
    path: Path, ns: str, imported: FrozenSet[str]
) -> Set[str]:
    py_modules = find_files(path)

    found = {m: set(extract_imports(m)).intersection(imported) for m in py_modules}
    filtered = {k: v for k, v in found.items() if v}

    fetched = (fetch_import_usages_in_module(k, ns, v) for k, v in filtered.items())

    return {i for f in fetched if f for i in f}
