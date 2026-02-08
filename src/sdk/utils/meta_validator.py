# src/sdk/utils/meta_validator.py
from typing import Dict, Any
from ..schemas.meta_schema import BaseMetaSchema


def validate_meta(data: Dict[str, Any]) -> BaseMetaSchema:
    """
    Valida metadata contra el schema oficial del SDK.
    """
    return BaseMetaSchema(**data)
