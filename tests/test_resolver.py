import pytest
from unittest.mock import MagicMock
from pathlib import Path
from bk.resolver import DependencyResolver
from bk.contracts import StorageBackend
from bk.exceptions import DependencyError

def test_resolve_success():
    storage = MagicMock(spec=StorageBackend)
    storage.resolve_dependency.return_value = Path("/libs/lib_core")
    
    resolver = DependencyResolver(storage)
    deps = {"lib_core": "^1.0.0"}
    
    resolved = resolver.resolve(deps)
    assert resolved["lib_core"] == Path("/libs/lib_core")

def test_resolve_failure():
    storage = MagicMock(spec=StorageBackend)
    storage.resolve_dependency.return_value = None
    
    resolver = DependencyResolver(storage)
    deps = {"lib_missing": "^1.0.0"}
    
    with pytest.raises(DependencyError):
        resolver.resolve(deps)
