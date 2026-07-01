import libcst as cst
from pathlib import Path
from typing import List, Union, Optional, Tuple, Any


def create_namespace_path(top_ns: str, current: str) -> str:
    top_ns_module_path = top_ns.replace("/", ".")
    return f"{top_ns_module_path}.{current}"


def extract_module_value(module_node: cst.BaseExpression) -> Optional[str]:
    if isinstance(module_node, cst.Name):
        return str(module_node.value)
    elif isinstance(module_node, cst.Attribute):
        parts = []
        current = module_node
        while isinstance(current, cst.Attribute):
            parts.append(str(current.attr.value))
            current = current.value
        if isinstance(current, cst.Name):
            parts.append(str(current.value))
            return ".".join(reversed(parts))
    return None


def create_new_module(module_value: str, top_ns: str) -> cst.BaseExpression:
    new_module_parts = create_namespace_path(top_ns, module_value).split(".")
    new_module = cst.Name(new_module_parts[0])
    for part in new_module_parts[1:]:
        new_module = cst.Attribute(value=new_module, attr=cst.Name(part))
    return new_module


def should_rewrite_module(module_value: str, ns: str) -> bool:
    return module_value == ns or module_value.startswith(f"{ns}.")


def mutate_import(node: cst.Import, ns: str, top_ns: str) -> Tuple[bool, cst.Import]:
    did_mutate = False
    new_aliases = []
    
    for alias in node.names:
        if alias.name.value == ns:
            did_mutate = True
            if alias.asname is None:
                new_alias = alias.with_changes(
                    asname=cst.AsName(cst.Name(str(alias.name.value)))
                )
            else:
                new_alias = alias
            new_name_parts = create_namespace_path(top_ns, str(alias.name.value)).split(".")
            new_name: cst.BaseExpression = cst.Name(new_name_parts[0])
            for part in new_name_parts[1:]:
                new_name = cst.Attribute(value=new_name, attr=cst.Name(part))
            new_alias = new_alias.with_changes(name=new_name)
            new_aliases.append(new_alias)
        else:
            new_aliases.append(alias)
    
    return did_mutate, node.with_changes(names=new_aliases)


def mutate_import_from(node: cst.ImportFrom, ns: str, top_ns: str) -> Tuple[bool, cst.ImportFrom]:
    if node.module and not node.relative:
        module_value = extract_module_value(node.module)
        
        if module_value and should_rewrite_module(module_value, ns):
            new_module = create_new_module(module_value, top_ns)
            return True, node.with_changes(module=new_module)
    
    return False, node


def process_import_node(node: cst.Import, ns: str, top_ns: str) -> Tuple[bool, cst.SimpleStatementLine]:
    mutated, new_node = mutate_import(node, ns, top_ns)
    return mutated, cst.SimpleStatementLine(body=[new_node])


def process_import_from_node(node: cst.ImportFrom, ns: str, top_ns: str) -> Tuple[bool, cst.SimpleStatementLine]:
    mutated, new_node = mutate_import_from(node, ns, top_ns)
    return mutated, cst.SimpleStatementLine(body=[new_node])


def process_subnode(subnode: cst.CSTNode, ns: str, top_ns: str) -> Tuple[bool, cst.CSTNode]:
    if isinstance(subnode, cst.Import):
        return mutate_import(subnode, ns, top_ns)
    elif isinstance(subnode, cst.ImportFrom):
        return mutate_import_from(subnode, ns, top_ns)
    return False, subnode


def process_simple_statement_line(node: cst.SimpleStatementLine, ns: str, top_ns: str) -> Tuple[bool, cst.SimpleStatementLine]:
    did_mutate = False
    new_body = []
    
    for subnode in node.body:
        mutated, new_node = process_subnode(subnode, ns, top_ns)
        if mutated:
            did_mutate = True
        new_body.append(new_node)
    
    return did_mutate, cst.SimpleStatementLine(body=new_body)


def rewrite(source: Path, ns: str, top_ns: str) -> bool:
    file_path = source.as_posix()

    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()

    tree = cst.parse_module(source_code)
    did_mutate = False
    new_body = []

    for node in tree.body:
        if isinstance(node, cst.SimpleStatementLine):
            mutated, new_node = process_simple_statement_line(node, ns, top_ns)
            if mutated:
                did_mutate = True
            new_body.append(new_node)
        else:
            new_body.append(node)

    if did_mutate:
        modified_tree = tree.with_changes(body=new_body)
        rewritten_source_code = modified_tree.code

        with open(file_path, "w", encoding="utf-8", newline="") as f:
            f.write(rewritten_source_code)

        return True

    return False


def rewrite_module(module: Path, ns: str, top_ns: str) -> Union[str, None]:
    was_rewritten = rewrite(module, ns, top_ns)

    return f"{module.parent.name}/{module.name}" if was_rewritten else None


def rewrite_modules(path: Path, ns: str, top_ns: str) -> List[str]:
    modules = path.glob("**/*.py")

    res = [rewrite_module(module, ns, top_ns) for module in modules]

    return [r for r in res if r]
