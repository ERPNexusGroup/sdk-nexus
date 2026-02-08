# src/sdk/utils/meta_parser.py
import ast
from pathlib import Path
from typing import Any, Dict
# from bk.exceptions import ValidationError


def parse_meta_file(meta_path: Path) -> Dict[str, Any]:
    """
    Extrae variables top-level de __meta__.py usando AST (100% seguro, sin ejecutar código)

    Soporta:
    - Literales simples (str, int, float, bool, None)
    - Listas de literales
    - Diccionarios de literales (para geo_restrictions, authors, etc.)
    - Listas de diccionarios (para authors)
    """
    if not meta_path.exists():
        raise FileNotFoundError(f"Archivo no encontrado: {meta_path}")

    try:
        tree = ast.parse(meta_path.read_text(encoding="utf-8"), filename=str(meta_path))
    except SyntaxError as e:
        raise ValidationError(
            f"Error de sintaxis en __meta__.py línea {e.lineno}: {e.msg}"
        )

    metadata = {}
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and not target.id.startswith("_"):
                try:
                    value = _ast_node_to_safe_value(node.value, meta_path, target.id)
                    metadata[target.id] = value
                except ValueError as e:
                    raise ValidationError(f"Error en __meta__.py línea {node.lineno}: {e}")

    if not metadata:
        raise ValidationError(f"__meta__.py no contiene variables top-level válidas")

    return metadata


def _ast_node_to_safe_value(node: ast.AST, meta_path: Path, var_name: str) -> Any:
    """Convierte nodo AST a valor Python seguro (solo literales)"""
    if isinstance(node, ast.Constant):
        return node.value

    elif isinstance(node, ast.List):
        return [_ast_node_to_safe_value(elt, meta_path, var_name) for elt in node.elts]

    elif isinstance(node, ast.Dict):
        keys = [_ast_node_to_safe_value(k, meta_path, var_name) for k in node.keys]
        values = [_ast_node_to_safe_value(v, meta_path, var_name) for v in node.values]
        return dict(zip(keys, values))

    elif isinstance(node, ast.Name):
        if node.id in ("True", "False", "None"):
            return {"True": True, "False": False, "None": None}[node.id]
        raise ValueError(
            f"Variable no permitida '{node.id}' en {var_name}. "
            f"Solo se permiten literales y True/False/None"
        )

    elif isinstance(node, ast.JoinedStr):
        raise ValueError(f"f-strings no permitidos en {var_name}")

    else:
        node_type = type(node).__name__
        raise ValueError(
            f"Tipo no soportado en {var_name}: {node_type} "
            f"(solo literales permitidos: str, int, float, bool, None, list, dict)"
        )