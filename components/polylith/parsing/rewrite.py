import ast
from pathlib import Path
from typing import List, Union


def create_namespace_path(top_ns: str, current: str) -> str:
    top_ns_module_path = top_ns.replace("/", ".")
    return f"{top_ns_module_path}.{current}"


def mutate_import(node: ast.Import, ns: str, top_ns: str) -> bool:
    did_mutate = False

    for alias in node.names:
        if alias.name == ns:
            alias.name = create_namespace_path(top_ns, alias.name)
            did_mutate = True

    return did_mutate


def mutate_import_from(node: ast.ImportFrom, ns: str, top_ns: str) -> bool:
    did_mutate = False

    if not node.module or node.level != 0:
        return did_mutate

    if node.module == ns or node.module.startswith(f"{ns}."):
        node.module = create_namespace_path(top_ns, node.module)
        did_mutate = True

    return did_mutate


def mutate_imports(node: ast.AST, ns: str, top_ns: str) -> bool:
    if isinstance(node, ast.Import):
        return mutate_import(node, ns, top_ns)

    if isinstance(node, ast.ImportFrom):
        return mutate_import_from(node, ns, top_ns)

    return False


def rewrite(source: Path, ns: str, top_ns: str) -> bool:
    file_path = source.as_posix()

    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), source.name)

    res = {mutate_imports(node, ns, top_ns) for node in ast.walk(tree)}

    if True in res:
        rewritten_source_code = ast.unparse(tree)  # type: ignore[attr-defined]

        with open(file_path, "w", encoding="utf-8", newline="") as f:
            f.write(rewritten_source_code)

        return True

    return False


def rewrite_module(module: Path, ns: str, top_ns: str) -> Union[str, None]:
    was_rewritten = rewrite(module, ns, top_ns)

    return f"{module.parent.name}/{module.name}" if was_rewritten else None


def rewrite_modules(path: Path, ns: str, top_ns: str) -> List[str]:
    """Rewrite modules in bricks with new top namespace

    returns a list of bricks that was rewritten
    """

    modules = path.glob("**/*.py")

    res = [rewrite_module(module, ns, top_ns) for module in modules]

    return [r for r in res if r]
