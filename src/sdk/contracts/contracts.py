from typing import Protocol, Optional
from pathlib import Path

class StorageBackend(Protocol):
    """Contrato para almacenamiento - implementado por CLI y Core"""
    
    def copy_files(self, source: Path, destination: Path) -> None:
        """Copia archivos desde el origen al destino."""
        ...

    def remove_files(self, path: Path) -> None:
        """Elimina archivos o directorios en la ruta especificada."""
        ...

    def register_component(self, path: Path, manifest: dict) -> None:
        """Registra un componente en el sistema."""
        ...

    def unregister_component(self, name: str) -> None:
        """Desregistra un componente del sistema."""
        ...

    def resolve_dependency(self, name: str, version_spec: str) -> Optional[Path]:
        """Resuelve la ruta de una dependencia basada en su nombre y especificación de versión."""
        ...
