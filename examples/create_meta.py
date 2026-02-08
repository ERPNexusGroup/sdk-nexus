from pathlib import Path

from sdk.meta_codegen import MetaGenerator

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR.parent / "src" / "sdk" / "templates"

OUTPUT_META = BASE_DIR / "demo" / "__meta__.py"

generator = MetaGenerator(TEMPLATES_DIR)

data = {
    "technical_name": "demo",
    "display_name": "demo",
    "component_type": "module",
    "package_type": "ui",
    "domain": "hospitality",
    "version": "0.1.0",
    "description": "Componente ERP NEXUS para reservas hoteleras",
}

generator.generate_and_write(
    OUTPUT_META,
    data
)

print("✅ __meta__.py generado correctamente")
