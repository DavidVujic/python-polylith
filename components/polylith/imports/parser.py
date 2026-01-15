import ast
from collections.abc import Iterable
from functools import lru_cache
from pathlib import Path
from typing import FrozenSet, List, Optional, Set, Tuple, Union

typing_ns = "typing"
type_checking = "TYPE_CHECKING"

WRAPPER_NODES = (ast.Await, ast.Expr, ast.NamedExpr, ast.Starred, ast.Subscript)
FN_NODES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)


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


def extract_api_part(path: str) -> str:
    return path.rsplit(".", 1)[-1]


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


def find_matching_usage(expr: ast.expr, options: dict) -> Optional[str]:
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
        found = api_map[root.id] if usage == root.id else usage

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


def extract_imports_and_flatten(py_modules: Iterable) -> Set[str]:
    return {i for m in py_modules for i in extract_imports(m)}


def is_python_file(path: Path) -> bool:
    return path.is_file() and path.suffix == ".py"


def find_files(path: Path) -> Iterable:
    return [path] if is_python_file(path) else path.rglob("*.py")


@lru_cache(maxsize=None)
def list_imports(path: Path) -> Set[str]:
    py_modules = find_files(path)

    return extract_imports_and_flatten(py_modules)


def fetch_all_imports(paths: Set[Path]) -> dict:
    rows = [{p.name: list_imports(p)} for p in paths]

    return {k: v for row in rows for k, v in row.items()}


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

    return extract_imports_and_flatten(filtered)


def fetch_excluded_imports(paths: Set[Path], excludes: Set[str]) -> dict:
    rows = [{p.name: list_excluded_imports(p, excludes)} for p in paths]

    return {k: v for row in rows for k, v in row.items()}


def extract_top_ns_from_imports(imports: Set[str]) -> Set:
    return {imp.split(".")[0] for imp in imports}


def extract_top_ns(import_data: dict) -> dict:
    return {k: extract_top_ns_from_imports(v) for k, v in import_data.items()}
