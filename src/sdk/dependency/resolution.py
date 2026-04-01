"""
Resolución de dependencias entre módulos.

Construye un plan de carga ordenado por dependencias,
sin asumir nada sobre instalación.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .resolver import DependencyResolver
from ..schemas.meta_schema import BaseMetaSchema
from ..utils.meta_parser import parse_meta_file
from ..exceptions import ValidationError


@dataclass(frozen=True)
class DependencyPlan:
    """
    Plan de resolución de dependencias.

    Contiene el orden en que los módulos deben cargarse/instalarse
    para respetar las dependencias declaradas.
    """
    load_order: List[str]
    components: Dict[str, BaseMetaSchema]
    optional_skipped: List[str]
    total: int
    paths_by_name: Dict[str, Path]


def resolve_dependencies(component_paths: List[Path]) -> DependencyPlan:
    """
    Resuelve el orden de dependencias para un conjunto de módulos.

    Todos los módulos referenciados en `depends` deben estar
    incluidos en component_paths.

    Args:
        component_paths: Lista de rutas a directorios de módulos

    Returns:
        DependencyPlan con el orden de carga

    Raises:
        ValidationError: Si falta un módulo o su metadata
        DependencyError: Si hay conflictos de versión o ciclos
    """
    resolver = DependencyResolver()
    paths_by_name: Dict[str, Path] = {}

    for path in component_paths:
        path = path.resolve()
        meta = parse_meta_file(path / "__meta__.py")
        name = meta.get("technical_name")
        if not name:
            raise ValidationError(f"Falta technical_name en {path / '__meta__.py'}")
        paths_by_name[name] = path
        resolver.load_component(path)

    result = resolver.resolve()

    return DependencyPlan(
        load_order=result["install_order"],
        components=result["components"],
        optional_skipped=result["optional_skipped"],
        total=result["total"],
        paths_by_name=paths_by_name,
    )
