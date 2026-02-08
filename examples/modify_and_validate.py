from pathlib import Path

from sdk.utils.meta_parser import parse_meta_file
from sdk.utils.meta_validator import validate_meta

META_PATH = Path(__file__).parent / "demo" / "__meta__.py"

metadata = parse_meta_file(META_PATH)

print("📦 metadata original cargada")

# Simular cambio manual del dev
metadata["version"] = "1.2.0"

validated = validate_meta(metadata)

print("✅ cambios válidos")
print(validated.version)
