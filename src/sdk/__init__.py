# src/sdk/__init__.py
"""
ERP NEXUS SDK
=============
SDK puro Python para definir y validar componentes compatibles con ERP NEXUS.
"""
__version__ = "1.0.0"

from .exceptions import (
    NexusSDKError,
    ValidationError,
    DependencyError,
    InstallationError,
)
from .contracts import StorageBackend
from .installer import TransactionalInstaller, InstallResult
from .registry import ComponentRegistry
from .dependency.install_plan import InstallPlan, build_install_plan
from .schemas.meta_schema import (
    ModuleMetaSchema,
    AppMetaSchema,
    BaseMetaSchema,
)
from .utils.meta_parser import parse_meta_file

# Exportar clases principales para API pública
from .validation.component_validator import ComponentValidator

# Definir API pública explícita
__all__ = [
    # Validación
    "ComponentValidator",
    "parse_meta_file",

    # Contratos y registry
    "StorageBackend",
    "ComponentRegistry",
    "TransactionalInstaller",
    "InstallResult",
    "InstallPlan",
    "build_install_plan",

    # Esquemas
    "ModuleMetaSchema",
    "AppMetaSchema",
    "BaseMetaSchema",

    # Excepciones
    "NexusSDKError",
    "ValidationError",
    "DependencyError",
    "InstallationError",
]
