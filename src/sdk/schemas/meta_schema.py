# src/sdk/schemas/meta_schema.py
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Dict, Optional, Literal, Any
from semantic_version import Version as SemVer, SimpleSpec


class AuthorInfo(BaseModel):
    """Información de un autor/contribuyente"""
    name: str = Field(..., min_length=2)
    role: Literal["author", "maintainer", "contributor"] = "contributor"
    email: Optional[str] = None
    website: Optional[str] = None


class GeoRestrictions(BaseModel):
    """Restricciones geográficas de disponibilidad"""
    include: List[str] = Field(default_factory=lambda: ["*"])
    exclude: List[str] = Field(default_factory=list)


class ExternalDependencies(BaseModel):
    """Dependencias externas (PyPI/binarios)"""
    python: List[str] = Field(default_factory=list)
    bin: List[str] = Field(default_factory=list)


class LifecycleHooks(BaseModel):
    """Hooks de ciclo de vida del componente"""
    pre_install: Optional[str] = None
    post_install: Optional[str] = None
    post_uninstall: Optional[str] = None


class RegistryFlags(BaseModel):
    """Flags de registro en el sistema ERP"""
    models: bool = False
    api: bool = False
    workers: bool = False
    tasks: bool = False


class BaseMetaSchema(BaseModel):
    """Esquema base minimalista para todos los componentes"""

    # ===== IDENTIDAD (OBLIGATORIO) =====
    technical_name: str = Field(
        ...,
        pattern=r'^[a-z][a-z0-9_]{2,50}$',
        description="Identificador único interno (snake_case)"
    )
    display_name: str = Field(..., min_length=3, max_length=100)
    component_type: Literal["module", "app"] = Field(...)
    package_type: Literal["core", "extension", "library", "integration", "ui"] = Field(...)
    domain: Optional[str] = None

    # ===== COMPATIBILIDAD (OBLIGATORIO) =====
    python: str = Field(">=3.11", description="Versión mínima de Python")
    erp_version: str = Field(">=0.1.0", description="Versión mínima del core ERP")
    geo_restrictions: GeoRestrictions = Field(default_factory=GeoRestrictions)

    # ===== DISTRIBUTION (OBLIGATORIO) =====
    version: str = Field(..., description="Versión semver (ej: 1.2.0)")
    license: str = Field("MIT", description="Licencia de distribución")
    keywords: List[str] = Field(default_factory=list, max_items=30)
    description: Optional[str] = Field(None, min_length=20, max_length=2000)
    website: Optional[str] = None
    authors: List[AuthorInfo] = Field(default_factory=list)

    # ===== DEPENDENCIAS (OPCIONAL) =====
    depends: List[str] = Field(default_factory=list)
    external_dependencies: ExternalDependencies = Field(default_factory=ExternalDependencies)
    dev_dependencies: List[str] = Field(default_factory=list)

    # ===== COMPORTAMIENTO (OPCIONAL) =====
    installable: bool = True
    auto_install: bool | List[str] = False
    demo_data: List[str] = Field(default_factory=list)
    lifecycle: LifecycleHooks = Field(default_factory=LifecycleHooks)

    # ===== AVANZADO (OPCIONAL) =====
    migration_version: Optional[str] = None
    load_priority: int = Field(50, ge=0, le=100)
    registry_flags: RegistryFlags = Field(default_factory=RegistryFlags)

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        try:
            SemVer(v)
            return v
        except ValueError:
            raise ValueError(f"Versión inválida '{v}' (debe ser semver: 1.2.0)")

    @field_validator("erp_version")
    @classmethod
    def validate_erp_version(cls, v: str) -> str:
        # Validar que sea especificación semver válida
        try:
            SimpleSpec(v)
            return v
        except ValueError:
            raise ValueError(f"Especificación de versión ERP inválida: '{v}'")

    @field_validator("python")
    @classmethod
    def validate_python_version(cls, v: str) -> str:
        # Validar especificación semver de Python (>=3.11, ~=3.12, etc.)
        try:
            SimpleSpec(v)
            return v
        except ValueError:
            raise ValueError(f"Especificación de versión Python inválida: '{v}'")

    @model_validator(mode="after")
    def validate_technical_name_vs_display_name(self) -> "BaseMetaSchema":
        """Genera display_name automáticamente si no se proporciona"""
        if not self.display_name:
            self.display_name = self.technical_name.replace("_", " ").title()
        return self


class ModuleMetaSchema(BaseMetaSchema):
    """Esquema para módulos principales"""
    component_type: Literal["module"] = "module"


class AppMetaSchema(BaseMetaSchema):
    """Esquema para aplicaciones"""
    component_type: Literal["app"] = "app"
