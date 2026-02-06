from pydantic import BaseModel, Field, field_validator
from semantic_version import Version, SimpleSpec # type: ignore

class DependencySchema(BaseModel):
    """Schema para validar dependencias."""
    name: str
    version_spec: str

    @field_validator("version_spec")
    @classmethod
    def validate_version_spec(cls, v: str) -> str:
        try:
            SimpleSpec(v)
        except ValueError:
            raise ValueError(f"Especificación de versión inválida: {v}")
        return v
