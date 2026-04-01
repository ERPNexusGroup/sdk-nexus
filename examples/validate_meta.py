"""Ejemplo: Validar un módulo existente."""
from pathlib import Path
from sdk import ComponentValidator
from sdk.exceptions import ValidationError

validator = ComponentValidator()

try:
    meta = validator.validate_component(Path(__file__).parent / "modules" / "sales")
    print(f"✅ Válido: {meta.technical_name} v{meta.version}")
    print(f"   Tipo: {meta.component_type} ({meta.package_type})")
    print(f"   Python: {meta.python}")
    print(f"   ERP: {meta.erp_version}")
except ValidationError as e:
    print(f"❌ Inválido: {e}")
