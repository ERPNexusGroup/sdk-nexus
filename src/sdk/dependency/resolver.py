from pathlib import Path
from typing import Dict, List

from .dependency_graph import DependencyGraph
from .errors import MissingDependencyError
from .version_resolver import VersionResolver

from ..exceptions import ValidationError
from ..schemas.meta_schema import BaseMetaSchema
from ..schemas.dependency_schema import DependencySchema
from ..utils.meta_parser import parse_meta_file


class DependencyResolver:
    """
    Resuelve dependencias entre componentes ERP Nexus
    """

    def __init__(self):
        self.graph = DependencyGraph()
        self.components: Dict[str, BaseMetaSchema] = {}

    # ------------------------------------------------------------------
    # LOAD
    # ------------------------------------------------------------------

    def load_component(self, path: Path) -> None:
        path = path.resolve()
        meta_path = path / "__meta__.py"

        if not meta_path.exists():
            raise FileNotFoundError(f"No se encontró __meta__.py en {path}")

        meta_dict = parse_meta_file(meta_path)
        meta = BaseMetaSchema(**meta_dict)

        if meta.technical_name != path.name:
            raise ValidationError(
                f"El directorio '{path.name}' no coincide con technical_name '{meta.technical_name}'"
            )

        self.components[meta.technical_name] = meta
        self.graph.add_node(meta.technical_name)

        for dep in self._normalize_dependencies(meta):
            self.graph.add_dependency(dep.name, meta.technical_name)

    # ------------------------------------------------------------------
    # NORMALIZATION
    # ------------------------------------------------------------------

    def _normalize_dependencies(
        self, meta: BaseMetaSchema
    ) -> List[DependencySchema]:

        normalized: List[DependencySchema] = []

        for dep in meta.depends:
            if isinstance(dep, str):
                normalized.append(DependencySchema(name=dep))
            elif isinstance(dep, dict):
                normalized.append(DependencySchema(**dep))
            else:
                raise ValidationError(
                    f"Dependencia inválida en {meta.technical_name}: {dep}"
                )

        return normalized

    # ------------------------------------------------------------------
    # RESOLVE
    # ------------------------------------------------------------------

    def resolve(self) -> Dict:
        """
        Devuelve un Install Plan (NO instala nada)
        """

        optional_skipped: List[str] = []

        # Validar dependencias
        for name, meta in self.components.items():
            for dep in self._normalize_dependencies(meta):

                if dep.name not in self.components:
                    if dep.optional:
                        optional_skipped.append(dep.name)
                        continue
                    raise MissingDependencyError(
                        f"{name} depende de '{dep.name}' que no está cargado"
                    )

                if dep.version:
                    VersionResolver.validate(
                        self.components[dep.name].version,
                        dep.version,
                        dep.name
                    )

        order = self.graph.topological_sort()

        return {
            "install_order": order,
            "components": {
                name: self.components[name] for name in order
            },
            "optional_skipped": optional_skipped,
            "total": len(order),
        }
