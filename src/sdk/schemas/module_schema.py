from typing import List, Dict, Optional
from pydantic import BaseModel, Field, EmailStr, field_validator
from semantic_version import Version # type: ignore
from ..constants import MODULE_PREFIX

class ModuleSchema(BaseModel):
    """Schema para validar module.json."""
    name: str
    version: str
    description: str
    author: str
    email: EmailStr
    keywords: List[str] = Field(default_factory=list)
    dependencies: Dict[str, str] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v.startswith(MODULE_PREFIX):
            raise ValueError(f"El nombre del módulo debe comenzar con '{MODULE_PREFIX}'")
        return v

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        try:
            Version(v)
        except ValueError:
            raise ValueError(f"Versión inválida: {v}")
        return v
