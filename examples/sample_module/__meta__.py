# tour_management/__meta__.py
"""
Módulo de Gestión de Tours para ERP NEXUS
Sistema completo para operadores turísticos con soporte para reservas, itinerarios y facturación.
"""

# ===== IDENTIDAD DEL COMPONENTE (OBLIGATORIO) =====
technical_name = "tour_management"          # Identificador único interno (snake_case)
display_name = "Gestión de Tours"           # Nombre visible en UI
component_type = "module"                   # "module" | "app"
package_type = "extension"                  # "core" | "extension" | "library" | "integration"
domain = "tourism"                          # Área funcional (opcional)

# ===== COMPATIBILIDAD DEL SISTEMA (OBLIGATORIO) =====
python = ">=3.11"                           # Versión mínima de Python
erp_version = ">=0.1.0"                     # Versión mínima del core ERP requerida
geo_restrictions = {                        # Restricciones geográficas (opcional)
    "include": ["*"],
    "exclude": []
}

# ===== DISTRIBUCIÓN Y METADATA (OBLIGATORIO) =====
version = "1.0.0"                           # Semantic versioning (obligatorio)
license = "MIT"                             # Licencia (opcional, default: MIT)
keywords = ["tour", "booking", "itinerary"] # Etiquetas de búsqueda
description = "Sistema de gestión de tours y reservas para operadores turísticos."
website = "https://erp-nexus.org/tour-management"

authors = [                                 # Lista de autores (opcional pero recomendado)
    {
        "name": "ERP NEXUS Team",
        "role": "author",
        "email": "dev@erp-nexus.org",
        "website": "https://erp-nexus.org"
    },
    {
        "name": "Walter",
        "role": "contributor",
        "email": "walter@tourcompany.ec"
    }
]

# ===== DEPENDENCIAS (OPCIONAL) =====
depends = ["core", "contacts"]              # Componentes Nexus requeridos
external_dependencies = {                   # Librerías externas (PyPI/binarios)
    "python": ["polars>=0.20.0", "qrcode>=7.4.0"],
    "bin": ["wkhtmltopdf"]
}
dev_dependencies = ["pytest>=8.0.0", "ruff>=0.3.0"]

# ===== COMPORTAMIENTO EN EL ERP (OPCIONAL) =====
installable = True                          # ¿Visible en UI para instalación?
auto_install = False                        # ¿Instalación automática si dependencias están presentes?
demo_data = ["demo/tours.json", "demo/itineraries.json"]

lifecycle = {                               # Hooks de ciclo de vida
    "pre_install": "tour_management.hooks.before_install",
    "post_install": "tour_management.hooks.after_install",
    "post_uninstall": "tour_management.hooks.cleanup"
}

# ===== CAMPOS AVANZADOS (OPCIONAL) =====
migration_version = "1.0.0"                 # Versión para control de migraciones
load_priority = 50                          # Prioridad de carga en registry (0-100)

registry_flags = {                          # Qué elementos registra el módulo
    "models": True,
    "api": True,
    "workers": False,
    "tasks": True
}