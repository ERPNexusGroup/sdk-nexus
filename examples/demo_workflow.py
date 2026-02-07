#!/usr/bin/env python3
"""
Demostración completa del flujo de trabajo del SDK ERP NEXUS:
1. Validación de módulos válidos e inválidos
2. Instalación con rollback automático
3. Desinstalación segura

Ejecutar desde la raíz del proyecto:
    python examples/demo_workflow.py
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
from sdk.exceptions import ValidationError
from sdk.installer import TransactionalInstaller
from examples.mock_storage import MockStorageBackend


def demo_validate_module(module_path: Path, console: Console):
    """Demuestra validación de un módulo"""
    console.print(Panel(f"🔍 VALIDANDO: {module_path.name}", style="bold blue"))

    validator = ComponentValidator()
    try:
        metadata = validator.validate_manifest(module_path)
        console.print(f"[green]✅ VÁLIDO[/green]: {metadata.technical_name} v{metadata.version}")

        # Mostrar resumen de metadata
        table = Table(show_header=False, box=None)
        table.add_row("Component Type", metadata.component_type)
        table.add_row("Package Type", metadata.package_type)
        table.add_row("Authors", ", ".join([a.name for a in metadata.authors]) if metadata.authors else "None")
        table.add_row("Dependencies", ", ".join(metadata.depends) if metadata.depends else "None")
        console.print(table)

        return True, metadata

    except ValidationError as e:
        console.print(f"[red]❌ INVÁLIDO[/red]: {module_path.name}")
        console.print(f"[red]Error: {e}[/red]")
        return False, None


def demo_install_with_rollback(console: Console):
    """Demuestra instalación con rollback automático en caso de fallo"""
    console.print(Panel("⚙️ INSTALACIÓN CON ROLLBACK AUTOMÁTICO", style="bold green"))

    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = Path(__file__).parent / "minimal_module"
        target_path = Path(tmpdir) / "installed_modules" / "hotel_reservations"

        # Crear storage mock
        storage = MockStorageBackend(Path(tmpdir) / "registry.json")
        installer = TransactionalInstaller(storage)

        # Simular instalación exitosa
        console.print("[blue]→ Instalando módulo válido...[/blue]")
        try:
            installer.install(source_path, target_path)
            console.print("[green]✅ Instalación exitosa[/green]")
            console.print(f"   Ruta: {target_path}")
            return True
        except Exception as e:
            console.print(f"[red]❌ Error inesperado: {e}[/red]")
            return False


def demo_install_failure_with_rollback(console: Console):
    """Demuestra rollback automático cuando falla la instalación"""
    console.print(Panel("⚠️ ESCENARIO: FALLO DURANTE INSTALACIÓN", style="bold yellow"))

    with tempfile.TemporaryDirectory() as tmpdir:
        # Crear storage mock que fallará en register_component
        class FailingStorage(MockStorageBackend):
            def register_component(self, path: Path, manifest: dict) -> None:
                raise Exception("Simulando fallo de base de datos durante registro")

        source_path = Path(__file__).parent / "minimal_module"
        target_path = Path(tmpdir) / "installed_modules" / "hotel_reservations"

        storage = FailingStorage(Path(tmpdir) / "registry.json")
        installer = TransactionalInstaller(storage)

        console.print("[blue]→ Intentando instalar (forzando fallo en registro)...[/blue]")
        try:
            installer.install(source_path, target_path)
            console.print("[red]❌ No debería llegar aquí[/red]")
            return False
        except Exception as e:
            console.print("[yellow]⚠️ Instalación fallida - activando rollback automático...[/yellow]")

            # Verificar que el rollback se ejecutó
            if not target_path.exists():
                console.print("[green]✅ Rollback exitoso: archivos eliminados[/green]")
            else:
                console.print("[red]❌ Rollback fallido: archivos residuales[/red]")
                return False

            if not storage.get_component("hotel_reservations"):
                console.print("[green]✅ Rollback exitoso: registro limpio[/green]")
                console.print("\n[bold green]🎉 SISTEMA EN ESTADO CONSISTENTE[/bold green]")
                return True
            else:
                console.print("[red]❌ Rollback fallido: registro inconsistente[/red]")
                return False


def demo_uninstall(console: Console):
    """Demuestra desinstalación segura"""
    console.print(Panel("🗑️ DESINSTALACIÓN SEGURA", style="bold magenta"))

    with tempfile.TemporaryDirectory() as tmpdir:
        source_path = Path(__file__).parent / "minimal_module"
        target_path = Path(tmpdir) / "installed_modules" / "hotel_reservations"

        storage = MockStorageBackend(Path(tmpdir) / "registry.json")
        installer = TransactionalInstaller(storage)

        # Primero instalar
        console.print("[blue]→ Instalando módulo para desinstalar...[/blue]")
        try:
            installer.install(source_path, target_path)
            console.print("[green]✅ Módulo instalado[/green]")
        except Exception as e:
            console.print(f"[red]❌ Falló instalación: {e}[/red]")
            return False

        # Verificar que existe
        if target_path.exists() and storage.get_component("hotel_reservations"):
            console.print("[blue]→ Desinstalando módulo...[/blue]")

            # Simular desinstalación
            storage.remove_files(target_path)
            storage.unregister_component("hotel_reservations")

            # Verificar que fue eliminado
            if not target_path.exists() and not storage.get_component("hotel_reservations"):
                console.print("[green]✅ Desinstalación exitosa[/green]")
                console.print("   - Archivos eliminados")
                console.print("   - Registro actualizado")
                return True
            else:
                console.print("[red]❌ Desinstalación incompleta[/red]")
                return False
        else:
            console.print("[red]❌ No se pudo instalar para desinstalar[/red]")
            return False


def main():
    console = Console()

    # Banner inicial
    console.print(Panel.fit(
        "[bold cyan]ERP NEXUS SDK - Demostración de Flujo de Trabajo[/bold cyan]\n"
        "Validación → Instalación → Rollback → Desinstalación",
        title="🚀 SDK DEMO",
        border_style="cyan"
    ))

    # 1. Validar módulo mínimo válido
    console.print("\n[bold]1. VALIDACIÓN DE MÓDULO VÁLIDO[/bold]")
    valid_minimal, meta_minimal = demo_validate_module(
        Path(__file__).parent / "minimal_module",
        console
    )

    if not valid_minimal:
        console.print("[red]❌ Falló validación del módulo mínimo - deteniendo demo[/red]")
        return 1

    console.print("\n[bold]Presiona Enter para continuar...[/bold]")
    input()

    # 2. Validar extensión reutilizable
    console.print("\n[bold]2. VALIDACIÓN DE EXTENSIÓN REUTILIZABLE[/bold]")
    valid_extension, meta_extension = demo_validate_module(
        Path(__file__).parent / "validation_dni_ec",
        console
    )

    if not valid_extension:
        console.print("[red]❌ Falló validación de la extensión - deteniendo demo[/red]")
        return 1

    console.print("\n[bold]Presiona Enter para continuar...[/bold]")
    input()

    # 3. Validar módulo inválido (debe fallar)
    console.print("\n[bold]3. VALIDACIÓN DE MÓDULO INVÁLIDO (debe fallar)[/bold]")
    valid_invalid, _ = demo_validate_module(
        Path(__file__).parent / "invalid_module",
        console
    )

    if valid_invalid:
        console.print("[red]❌ ERROR: El módulo inválido fue aceptado (debería fallar)[/red]")
        return 1
    else:
        console.print("[green]✅ Validación correcta: rechazó módulo inválido[/green]")

    console.print("\n[bold]Presiona Enter para continuar...[/bold]")
    input()

    # 4. Instalación exitosa
    console.print("\n[bold]4. INSTALACIÓN EXITOSA[/bold]")
    if not demo_install_with_rollback(console):
        console.print("[red]❌ Falló instalación exitosa[/red]")
        return 1

    console.print("\n[bold]Presiona Enter para continuar...[/bold]")
    input()

    # 5. Rollback automático en fallo
    console.print("\n[bold]5. ROLLBACK AUTOMÁTICO EN FALLO[/bold]")
    if not demo_install_failure_with_rollback(console):
        console.print("[red]❌ Falló demostración de rollback[/red]")
        return 1

    console.print("\n[bold]Presiona Enter para continuar...[/bold]")
    input()

    # 6. Desinstalación segura
    console.print("\n[bold]6. DESINSTALACIÓN SEGURA[/bold]")
    if not demo_uninstall(console):
        console.print("[red]❌ Falló desinstalación[/red]")
        return 1

    # Resumen final
    console.print("\n")
    console.print(Panel.fit(
        "[bold green]✅ DEMO COMPLETADO EXITOSAMENTE[/bold green]\n\n"
        "El SDK ERP NEXUS proporciona:\n"
        "• Validación estática 100% segura (sin ejecutar código)\n"
        "• Instalación transaccional con rollback automático garantizado\n"
        "• Desinstalación limpia sin residuos\n"
        "• Soporte para extensiones reutilizables entre módulos\n\n"
        "[bold]Próximos pasos:[/bold]\n"
        "1. Crea tu propio módulo con nexus-cli create\n"
        "2. Implementa tu StorageBackend para producción\n"
        "3. Usa el CLI 'nexus' para gestión simplificada",
        title="🎉 Resumen",
        border_style="green"
    ))

    return 0


if __name__ == "__main__":
    sys.exit(main())