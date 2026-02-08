from typing import Dict, Optional
from pathlib import Path
from semantic_version import Version, SimpleSpec # type: ignore
from sdk.contracts import StorageBackend
from sdk.exceptions import DependencyError

class DependencyResolver:
    """Resolutor de dependencias."""

    def __init__(self, storage: StorageBackend):
        self.storage = storage

    def resolve(self, dependencies: Dict[str, str]) -> Dict[str, Path]:
        """Resuelve un conjunto de dependencias."""
        resolved_paths = {}
        for name, version_spec in dependencies.items():
            path = self.storage.resolve_dependency(name, version_spec)
            if not path:
                raise DependencyError(f"No se pudo resolver la dependencia: {name} ({version_spec})")
            resolved_paths[name] = path
        return resolved_paths
