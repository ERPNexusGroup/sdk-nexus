# -*- coding: utf-8 -*-
"""
Módulo ERP NEXUS - {{ technical_name }}
=========================

¡Bienvenido! Este archivo define la metadata de tu componente.
NO ejecutes código aquí - solo asigna valores a las variables.
"""

__meta_schema_version__ = "{{ meta_schema_version }}"
__meta_template_version__ = "{{ meta_template_version }}"


# ════════════════════════════════════════════════════════════════════════════════
# 🔑 IDENTIDAD DEL COMPONENTE
# ════════════════════════════════════════════════════════════════════════════════

technical_name = "{{ technical_name }}"
display_name = "{{ display_name }}"
component_type = "{{ component_type }}"
package_type = "{{ package_type }}"
domain = "{{ domain }}"

# ════════════════════════════════════════════════════════════════════════════════
# ⚙️ COMPATIBILIDAD
# ════════════════════════════════════════════════════════════════════════════════

python = "{{ python }}"
erp_version = "{{ erp_version }}"

geo_restrictions = {
    "include": ["*"],
    "exclude": []
}

# ════════════════════════════════════════════════════════════════════════════════
# 📦 DISTRIBUCIÓN
# ════════════════════════════════════════════════════════════════════════════════

version = "{{ version }}"
license = "MIT"
keywords = []
description = "{{ description }}"
website = ""
authors = []

# ════════════════════════════════════════════════════════════════════════════════
# 🔗 DEPENDENCIAS
# ════════════════════════════════════════════════════════════════════════════════

depends = []
external_dependencies = {"python": [], "bin": []}
dev_dependencies = []

# ════════════════════════════════════════════════════════════════════════════════
# 🧠 COMPORTAMIENTO
# ════════════════════════════════════════════════════════════════════════════════

installable = True
auto_install = False
demo_data = []
lifecycle = {}

# ════════════════════════════════════════════════════════════════════════════════
# 🧬 AVANZADO
# ════════════════════════════════════════════════════════════════════════════════

migration_version = "1.0.0"
load_priority = 50
registry_flags = {}
