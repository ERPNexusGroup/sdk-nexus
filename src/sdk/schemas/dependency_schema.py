# src/sdk/schemas/dependency_schema.py
from pydantic import BaseModel, Field
from typing import Optional


class DependencySchema(BaseModel):
    """
    Representa una dependencia declarada por un componente.
    """
    name: str = Field(..., min_length=2)
    version: Optional[str] = None
    optional: bool = False
