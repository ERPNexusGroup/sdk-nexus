from typing import Dict, Optional
from pydantic import BaseModel, Field, field_validator
from semantic_version import Version # type: ignore
from ..constants import APP_PREFIX

class AppSchema(BaseModel):
    """Schema para validar app.json."""
    name: str
    version: str
    description: str
    parent_module: str
    dependencies: Dict[str, str] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.startswith(APP_PREFIX):
            raise ValueError(f"El nombre de la aplicación debe comenzar con '{APP_PREFIX}'")
        return v

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        try:
            Version(v)
        except ValueError:
            raise ValueError(f"Versión inválida: {v}")
        return v
