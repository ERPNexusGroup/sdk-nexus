from pathlib import Path
from sdk.dependency import DependencyResolver

BASE_DIR = Path(__file__).parent

resolver = DependencyResolver()

resolver.load_component(BASE_DIR / "modules" / "base")
resolver.load_component(BASE_DIR / "modules" / "sales")
resolver.load_component(BASE_DIR / "modules" / "inventory")

plan = resolver.resolve()

print("INSTALL ORDER:")
for name in plan["install_order"]:
    print(" -", name)

print("\nOPTIONAL SKIPPED:", plan["optional_skipped"])
print("TOTAL:", plan["total"])
