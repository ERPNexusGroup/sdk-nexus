"""
Excepciones del SDK Nexus.

Jerarquía:
  NexusSDKError (base)
  ├── ValidationError     — módulo no pasa validación
  ├── DependencyError     — problema con dependencias
  ├── PackagingError      — error al empaquetar
  └── ScaffoldError       — error al crear estructura de módulo
"""


class NexusSDKError(Exception):
    """Clase base para excepciones del SDK Nexus."""
    pass


class ValidationError(NexusSDKError):
    """Error durante la validación de un componente."""
    pass


class DependencyError(NexusSDKError):
    """Error relacionado con la resolución de dependencias."""
    pass


class PackagingError(NexusSDKError):
    """Error durante el empaquetado de un componente."""
    pass


class ScaffoldError(NexusSDKError):
    """Error durante la creación de la estructura de un módulo."""
    pass
