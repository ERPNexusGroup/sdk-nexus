#!/usr/bin/env python3
"""
Ejemplo práctico: Crear, validar e instalar un módulo con el SDK ERP NEXUS

Este script demuestra el flujo completo:
1. Crear estructura de módulo mínimo
2. Validar metadata con el SDK
3. Instalar con rollback automático
4. Desinstalar limpiamente

Ejecutar desde la raíz del proyecto:
    python examples/create_module_example.py
"""

import sys
import tempfile
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Añadir src al path para importar el SDK
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sdk.validator import ComponentValidator
from sdk.installer import TransactionalInstaller
from sdk.exceptions import ValidationError, InstallationError
from examples.mock_storage import MockStorageBackend  # Usa tu mock_storage existente


def create_minimal_module(base_path: Path) -> Path:
    """Crea estructura mínima de un módulo hotelero válido"""
    module_dir = base_path / "my_hotel_module"
    module_dir.mkdir(exist_ok=True)

    # Crear __meta__.py mínimo válido (7 campos obligatorios)
    meta_content = '''technical_name = "my_hotel_module"
display_name = "Mi Módulo Hotelero"
component_type = "module"
package_type = "extension"
python = ">=3.11"
erp_version = ">=0.1.0"
version = "1.0.0"
'''
    (module_dir / "__meta__.py").write_text(meta_content, encoding="utf-8")

    # Crear __init__.py (obligatorio para que sea importable)
    (module_dir / "__init__.py").write_text("# Módulo hotelero mínimo\n", encoding="utf-8")

    # Crear estructura mínima de core
    core_dir = module_dir / "core"
    core_dir.mkdir(exist_ok=True)
    (core_dir / "__init__.py").write_text("", encoding="utf-8")
    (core_dir / "models.py").write_text("# Modelos Django\n", encoding="utf-8")

    return module_dir


def validate_module(module_path: Path, console: Console) -> bool:
    """Valida el módulo usando el SDK"""
    console.print(Panel("🔍 VALIDANDO MÓDULO CON SDK", style="bold blue"))

    validator = ComponentValidator()
    try:
        metadata = validator.validate_manifest(module_path)

        console.print(f"[green]✅ MÓDULO VÁLIDO[/green]: {metadata.technical_name} v{metadata.version}")

        # Mostrar resumen
        table = Table(show_header=False, box=None)
        table.add_row("Technical Name", metadata.technical_name)
        table.add_row("Display Name", metadata.display_name)
        table.add_row("Component Type", metadata.component_type)
        table.add_row("Package Type", metadata.package_type)
        table.add_row("Python", metadata.python)
        table.add_row("ERP Version", metadata.erp_version)
        console.print(table)

        return True

    except ValidationError as e:
        console.print(f"[red]❌ MÓDULO INVÁLIDO[/red]")
        console.print(f"[red]Error: {e}[/red]")
        return False


def install_module(module_path: Path, target_path: Path, console: Console) -> bool:
    """Instala el módulo con rollback automático"""
    console.print(Panel("⚙️ INSTALANDO MÓDULO (con rollback automático)", style="bold green"))

    storage = MockStorageBackend(target_path.parent / "registry.json")
    installer = TransactionalInstaller(storage)

    try:
        installer.install(module_path, target_path)
        console.print(f"[green]✅ INSTALACIÓN EXITOSA[/green]")
        console.print(f"   Ruta: {target_path}")
        console.print(f"   Registrado: {storage.get_component('my_hotel_module') is not None}")
        return True

    except InstallationError as e:
        console.print(f"[red]❌ ERROR DE INSTALACIÓN[/red]")
        console.print(f"[red]{e}[/red]")
        return False


def uninstall_module(target_path: Path, console: Console) -> bool:
    """Desinstala el módulo limpiamente"""
    console.print(Panel("🗑️ DESINSTALANDO MÓDULO", style="bold magenta"))

    storage = MockStorageBackend(target_path.parent / "registry.json")

    # Eliminar archivos
    if target_path.exists():
        storage.remove_files(target_path)

    # Eliminar registro
    storage.unregister_component("my_hotel_module")

    # Verificar limpieza
    if not target_path.exists() and not storage.get_component("my_hotel_module"):
        console.print("[green]✅ DESINSTALACIÓN EXITOSA[/green]")
        console.print("   - Archivos eliminados")
        console.print("   - Registro actualizado")
        return True
    else:
        console.print("[red]❌ DESINSTALACIÓN INCOMPLETA[/red]")
        return False


def main():
    console = Console()

    # Banner inicial
    console.print(Panel.fit(
        "[bold cyan]ERP NEXUS SDK - Ejemplo de Creación de Módulo[/bold cyan]\n"
        "Flujo completo: Crear → Validar → Instalar → Desinstalar",
        title="🏨 Ejemplo Práctico",
        border_style="cyan"
    ))

    # 1. Crear módulo mínimo
    console.print("\n[bold]1. CREANDO MÓDULO MÍNIMO[/bold]")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)

        module_path = create_minimal_module(tmp_path)
        console.print(f"[blue]→ Módulo creado en:[/blue] {module_path}")
        console.print(f"[blue]→ Contenido de __meta__.py:[/blue]")
        console.print((module_path / "__meta__.py").read_text())

        console.print("\n[bold]Presiona Enter para continuar...[/bold]")
        input()

        # 2. Validar módulo
        console.print("\n[bold]2. VALIDANDO MÓDULO[/bold]")
        if not validate_module(module_path, console):
            console.print("[red]❌ Validación fallida - abortando[/red]")
            return 1

        console.print("\n[bold]Presiona Enter para continuar...[/bold]")
        input()

        # 3. Instalar módulo
        console.print("\n[bold]3. INSTALANDO MÓDULO[/bold]")
        target_path = tmp_path / "installed" / "my_hotel_module"
        if not install_module(module_path, target_path, console):
            console.print("[red]❌ Instalación fallida[/red]")
            return 1

        console.print("\n[bold]Presiona Enter para continuar...[/bold]")
        input()

        # 4. Desinstalar módulo
        console.print("\n[bold]4. DESINSTALANDO MÓDULO[/bold]")
        if not uninstall_module(target_path, console):
            console.print("[red]❌ Desinstalación fallida[/red]")
            return 1

        # Resumen final
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✅ FLUJO COMPLETO EXITOSO[/bold green]\n\n"
            "El SDK ERP NEXUS permite:\n"
            "• Crear módulos con solo 7 campos obligatorios\n"
            "• Validar metadata sin ejecutar código (AST parsing seguro)\n"
            "• Instalar con rollback automático garantizado\n"
            "• Desinstalar limpiamente sin residuos\n\n"
            "[bold]Siguiente paso:[/bold]\n"
            "Extiende __meta__.py con campos opcionales:\n"
            "  - authors, keywords, dependencies, etc.",
            title="🎉 Resumen",
            border_style="green"
        ))

    return 0


if __name__ == "__main__":
    sys.exit(main())