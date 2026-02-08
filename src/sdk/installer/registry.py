from typing import Dict, Any, Optional
from pathlib import Path
import json

class ComponentRegistry:
    """Manejador del registro de componentes instalados."""
    
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self._registry: Dict[str, Any] = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if not self.registry_path.exists():
            return {}
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}

    def save_registry(self) -> None:
        """Guarda el estado actual del registro en disco."""
        with open(self.registry_path, 'w', encoding='utf-8') as f:
            json.dump(self._registry, f, indent=2)

    def register(self, name: str, metadata: Dict[str, Any]) -> None:
        """Registra un componente."""
        self._registry[name] = metadata
        self.save_registry()

    def unregister(self, name: str) -> None:
        """Elimina un componente del registro."""
        if name in self._registry:
            del self._registry[name]
            self.save_registry()

    def get_component(self, name: str) -> Optional[Dict[str, Any]]:
        """Obtiene metadatos de un componente."""
        return self._registry.get(name)

    def list_components(self) -> Dict[str, Any]:
        """Lista todos los componentes registrados."""
        return self._registry
