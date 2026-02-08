import pytest
from unittest.mock import MagicMock
from pathlib import Path
from bk.installer import TransactionalInstaller
from bk.contracts import StorageBackend

class MockStorage(StorageBackend):
    def copy_files(self, source: Path, destination: Path) -> None:
        pass
    def remove_files(self, path: Path) -> None:
        pass
    def register_component(self, path: Path, manifest) -> None:
        pass
    def unregister_component(self, name: str) -> None:
        pass
    def resolve_dependency(self, name: str, version_spec: str):
        return Path("/tmp/dep")

def test_installer_rollback(tmp_path):
    storage = MockStorage()
    storage.copy_files = MagicMock(side_effect=Exception("Copy failed"))
    storage.remove_files = MagicMock()
    
    installer = TransactionalInstaller(storage)
    
    # Crear un módulo válido para intentar instalar
    source = tmp_path / "mod_source"
    source.mkdir()
    with open(source / "__meta__.py", "w") as f:
        f.write('{"name": "mod_test", "version": "1.0.0", "description": "d", "author": "a", "email": "a@a.com"}')
        
    target = tmp_path / "mod_target"
    
    with pytest.raises(Exception):
        installer.install(source, target)
        
    # Verificar que se llamó al rollback (remove_files)
    storage.remove_files.assert_called_once()
