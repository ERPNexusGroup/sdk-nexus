"""Ejemplo: Crear metadata para un módulo usando Pydantic."""
from sdk import BaseMetaSchema

# Crear un esquema válido programáticamente
meta = BaseMetaSchema(
    technical_name="hotel_reservations",
    display_name="Hotel Reservations",
    component_type="module",
    package_type="extension",
    domain="hospitality",
    version="0.1.0",
    description="Sistema de reservas hoteleras para ERP Nexus",
    keywords=["hotel", "reservations", "booking"],
    depends=["core_users"],
)

print(f"✅ Módulo válido: {meta.technical_name}")
print(f"   Versión: {meta.version}")
print(f"   Dominio: {meta.domain}")
print(f"   Dependencias: {meta.depends}")

# Exportar como dict
data = meta.model_dump()
print(f"\n📋 Datos: {data}")
