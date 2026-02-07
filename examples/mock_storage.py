# examples/mock_storage.py
"""
Implementación mock de StorageBackend para testing del SDK ERP NEXUS
Simula operaciones de almacenamiento en memoria/temporal sin afectar el sistema real.
"""

from pathlib import Path
import shutil
from typing import Optional, Dict, Any
from sdk.contracts import StorageBackend


class MockStorageBackend(StorageBackend):
    """
    Implementación mock de StorageBackend para testing

    Características:
    - Usa directorio temporal para simulación de filesystem
    - Registro en memoria (persistente durante la ejecución)
    - Rollback automático en caso de fallo
    - Sin efectos secundarios en el sistema real
    """

    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path("/tmp/nexus_mock_storage")
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Registro en memoria
        self._registry: Dict[str, Dict[str, Any]] = {}
        self._installed_paths: Dict[str, Path] = {}
        self._transactions: Dict[str, Dict[str, Any]] = {}

    def copy_files(self, source: Path, destination: Path) -> None:
        """Copia archivos recursivamente"""
        if not source.exists():
            raise FileNotFoundError(f"Origen no encontrado: {source}")

        if destination.exists():
            shutil.rmtree(destination)

        shutil.copytree(source, destination)

    def remove_files(self, path: Path) -> None:
        """Elimina archivos/directorios recursivamente"""
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    def register_component(self, path: Path, manifest: dict) -> None:
        """Registra componente en el sistema simulado"""
        technical_name = manifest.get("technical_name", manifest.get("name", "unknown"))

        # Validar campos obligatorios
        required_fields = ["technical_name", "version", "component_type"]
        missing = [f for f in required_fields if f not in manifest]
        if missing:
            raise ValueError(f"Manifest incompleto. Faltan campos: {', '.join(missing)}")

        # Registrar en memoria
        self._registry[technical_name] = {
            "name": technical_name,
            "version": manifest["version"],
            "path": str(path),
            "component_type": manifest["component_type"],
            "package_type": manifest.get("package_type", "extension"),
            "installed_at": "2024-05-22T10:00:00",
            "status": "active"
        }
        self._installed_paths[technical_name] = path

    def unregister_component(self, name: str) -> None:
        """Elimina registro del componente"""
        if name in self._registry:
            del self._registry[name]
        if name in self._installed_paths:
            del self._installed_paths[name]

    def resolve_dependency(self, name: str, version_spec: str) -> Optional[Path]:
        """Resuelve dependencias (simulado para testing)"""
        # Simular dependencias conocidas
        known_dependencies = {
            "validation_dni_ec": "/opt/nexus/components/validation_dni_ec",
            "sri_connector": "/opt/nexus/components/sri_connector",
            "core": "/opt/nexus/components/core",
            "contacts": "/opt/nexus/components/contacts"
        }

        if name in known_dependencies:
            return Path(known_dependencies[name])

        # Simular resolución exitosa con ruta ficticia
        return Path(f"/opt/nexus/components/{name}")

    def get_component_path(self, name: str) -> Optional[Path]:
        """Obtiene ruta de componente instalado"""
        return self._installed_paths.get(name)

    def get_component(self, name: str) -> Optional[Dict[str, Any]]:
        """Obtiene metadata de componente instalado"""
        return self._registry.get(name)

    def start_transaction(self, transaction_id: str) -> None:
        """Inicia una transacción (para rollback)"""
        self._transactions[transaction_id] = {
            "started_at": "2024-05-22T10:00:00",
            "components_before": self._registry.copy(),
            "paths_before": self._installed_paths.copy()
        }

    def rollback_transaction(self, transaction_id: str) -> bool:
        """Realiza rollback de una transacción"""
        if transaction_id not in self._transactions:
            return False

        snapshot = self._transactions[transaction_id]
        self._registry = snapshot["components_before"].copy()
        self._installed_paths = snapshot["paths_before"].copy()
        del self._transactions[transaction_id]
        return True