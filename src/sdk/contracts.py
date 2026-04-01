"""
Contratos del ecosistema ERP Nexus.

Define las interfaces que los módulos DEBEN o PUEDEN implementar
para integrarse correctamente con el ERP.
"""
from __future__ import annotations

from typing import Protocol, Optional, runtime_checkable


@runtime_checkable
class ModuleContract(Protocol):
    """
    Contrato base que todo módulo ERP Nexus debe cumplir.

    No necesitas heredar de esta clase — solo implementa los métodos.
    El SDK la usa para verificar que tu módulo es válido.
    """

    @staticmethod
    def get_meta() -> dict:
        """Retorna la metadata del módulo (desde __meta__.py)."""
        ...

    @staticmethod
    def get_version() -> str:
        """Retorna la versión semver del módulo."""
        ...


@runtime_checkable
class EventProvider(Protocol):
    """
    Contrato para módulos que EMITEN eventos al Event Bus.

    Un módulo que implementa esto puede comunicarse con otros
    módulos sin dependencia directa.
    """

    @staticmethod
    def get_events() -> list[str]:
        """Retorna lista de eventos que este módulo emite."""
        ...

    @staticmethod
    def get_event_handlers() -> dict[str, str]:
        """
        Retorna mapeo de eventos a handlers.
        Formato: {"event.type": "module.path.handler_function"}
        """
        ...


@runtime_checkable
class MigrationProvider(Protocol):
    """
    Contrato para módulos que tienen migraciones de base de datos.
    """

    @staticmethod
    def get_migrations_path() -> str:
        """Retorna la ruta al directorio de migraciones."""
        ...


@runtime_checkable
class APIProvider(Protocol):
    """
    Contrato para módulos que exponen endpoints de API.
    """

    @staticmethod
    def get_api_routes() -> list[dict]:
        """
        Retorna las rutas API que este módulo expone.
        Formato: [{"path": "/invoices", "method": "GET", "handler": "..."}]
        """
        ...
