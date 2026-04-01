"""
SDK Nexus — Dev Toolkit para ERP Nexus.

Herramientas para desarrolladores que crean módulos
compatibles con el ecosistema ERP Nexus.

Uso:
    from sdk import ComponentValidator, ModuleMetaSchema

    # Validar un módulo
    validator = ComponentValidator()
    meta = validator.validate_component(Path("./mi_modulo"))

    # Verificar contratos
    from sdk.contracts import ModuleContract, EventProvider
"""
__version__ = "1.1.0"

from .exceptions import (
    NexusSDKError,
    ValidationError,
    DependencyError,
    PackagingError,
    ScaffoldError,
)
from .contracts import (
    ModuleContract,
    EventProvider,
    MigrationProvider,
    APIProvider,
)
from .schemas.meta_schema import (
    ModuleMetaSchema,
    AppMetaSchema,
    BaseMetaSchema,
)
from .utils.meta_parser import parse_meta_file
from .validation.component_validator import ComponentValidator

__all__ = [
    # Version
    "__version__",

    # Validación
    "ComponentValidator",
    "parse_meta_file",

    # Contratos
    "ModuleContract",
    "EventProvider",
    "MigrationProvider",
    "APIProvider",

    # Esquemas
    "ModuleMetaSchema",
    "AppMetaSchema",
    "BaseMetaSchema",

    # Excepciones
    "NexusSDKError",
    "ValidationError",
    "DependencyError",
    "PackagingError",
    "ScaffoldError",
]
