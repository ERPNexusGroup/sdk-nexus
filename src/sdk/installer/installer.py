from pathlib import Path
from typing import Optional
from sdk.contracts import StorageBackend
from sdk.validation.validator import ComponentValidator
from sdk.installer.resolver import DependencyResolver
from sdk.exceptions import InstallationError, ValidationError, DependencyError

class TransactionalInstaller:
    """Instalador transaccional con rollback."""

    def __init__(self, storage: StorageBackend):
        self.storage = storage
        self.validator = ComponentValidator()
        self.resolver = DependencyResolver(storage)

    def install(self, source_path: Path, target_path: Path) -> None:
        """Instala un componente de manera transaccional."""
        manifest_path = self._find_manifest(source_path)
        if not manifest_path:
             raise InstallationError(f"No se encontró un manifiesto válido en {source_path}")

        try:
            # 1. Validar componente
            manifest = self.validator.validate_manifest(manifest_path)
            
            # 2. Resolver dependencias (simulado por ahora, solo verifica existencia)
            if hasattr(manifest, 'dependencies'):
                 self.resolver.resolve(manifest.dependencies)

            # 3. Copiar archivos (con rollback implícito si falla)
            self._perform_install(source_path, target_path, manifest)

        except (ValidationError, DependencyError) as e:
            raise InstallationError(f"Fallo en la pre-instalación: {e}")
        except Exception as e:
            # Rollback manual si es necesario (aquí simplificado)
            self._rollback(target_path, getattr(manifest, 'name', 'unknown'))
            raise InstallationError(f"Fallo durante la instalación: {e}")

    def _find_manifest(self, source_path: Path) -> Optional[Path]:
        for filename in ["__meta__.py", "app.json", "lib.json"]:
            path = source_path / filename
            if path.exists():
                return path
        return None

    def _perform_install(self, source: Path, target: Path, manifest) -> None:
        # Implementación real de copia y registro
        try:
            self.storage.copy_files(source, target)
            self.storage.register_component(target, manifest.model_dump())
        except Exception as e:
            raise e

    def _rollback(self, target: Path, component_name: str) -> None:
        """Revierte los cambios realizados."""
        try:
            self.storage.remove_files(target)
            self.storage.unregister_component(component_name)
        except Exception:
            # Log error durante rollback
            pass
