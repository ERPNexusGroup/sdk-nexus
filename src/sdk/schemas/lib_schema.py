from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator
from semantic_version import Version # type: ignore
from ..constants import LIB_PREFIXES

class LibSchema(BaseModel):
    """Schema para validar lib.json."""
    name: str
    version: str
    description: str
    standalone: bool = False
    dependencies: Dict[str, str] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not any(v.startswith(prefix) for prefix in LIB_PREFIXES):
            raise ValueError(f"El nombre de la librería debe comenzar con alguno de: {LIB_PREFIXES}")
        return v

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        try:
            Version(v)
        except ValueError:
            raise ValueError(f"Versión inválida: {v}")
        return v
