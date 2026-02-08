from pathlib import Path

from sdk.utils.meta_parser import parse_meta_file
from sdk.utils.meta_validator import validate_meta

META_PATH = Path(__file__).parent / "demo" / "__meta__.py"

metadata = parse_meta_file(META_PATH)

# romper schema
metadata["technical_name"] = ""

try:
    validate_meta(metadata)
except Exception as e:
    print("❌ validación falló correctamente")
    print(e)
