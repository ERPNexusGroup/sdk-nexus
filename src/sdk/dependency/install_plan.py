from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .resolver import DependencyResolver
from ..schemas.meta_schema import BaseMetaSchema
from ..utils.meta_parser import parse_meta_file
from ..exceptions import ValidationError


@dataclass(frozen=True)
class InstallPlan:
    install_order: List[str]
    components: Dict[str, BaseMetaSchema]
    optional_skipped: List[str]
    total: int
    paths_by_name: Dict[str, Path]


def build_install_plan(component_paths: List[Path]) -> InstallPlan:
    """
    Construye un plan de instalación ordenado por dependencias.
    Requiere que todas las dependencias estén incluidas en component_paths.
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

    return InstallPlan(
        install_order=result["install_order"],
        components=result["components"],
        optional_skipped=result["optional_skipped"],
        total=result["total"],
        paths_by_name=paths_by_name,
    )
