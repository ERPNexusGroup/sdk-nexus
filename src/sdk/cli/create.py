"""
Comando: sdk-nexus create <nombre>

Crea un módulo nuevo con estructura base y __meta__.py válido.
"""
from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from ..validation.component_validator import ComponentValidator
from ..exceptions import ValidationError

console = Console()


@click.command()
@click.argument("name")
@click.option(
    "--type", "component_type",
    default="module",
    type=click.Choice(["module", "app"]),
    help="Tipo de componente (default: module)",
)
@click.option(
    "--path", "-p", default=None,
    help="Directorio donde crear el módulo (default: directorio actual)",
)
@click.option(
    "--minimal", "-m", is_flag=True,
    help="Solo crear __meta__.py sin estructura de directorios",
)
@click.option(
    "--domain", "-d", default="custom",
    help="Dominio funcional (ej: accounting, hospitality, inventory)",
)
def create(
    name: str,
    component_type: str,
    path: str | None,
    minimal: bool,
    domain: str,
):
    """
    Crea un módulo ERP Nexus con metadata válida y estructura base.

    Ejemplos:

      sdk-nexus create hotel_reservations --type=module

      sdk-nexus create accounting_ec --domain=accounting --minimal
    """
    # Validar nombre
    import re
    if not re.match(r'^[a-z][a-z0-9_]{2,50}$', name):
        console.print(
            f"[red]✗ Nombre inválido: '{name}'[/red]\n"
            f"  Debe ser snake_case: minúsculas, números y guiones bajos\n"
            f"  Ejemplo válido: hotel_reservations"
        )
        sys.exit(1)

    base_path = Path(path) if path else Path.cwd()
    component_dir = base_path / name

    if component_dir.exists():
        console.print(f"[red]✗ Ya existe: {component_dir}[/red]")
        sys.exit(1)

    # Crear directorio
    component_dir.mkdir(parents=True)
    console.print(f"📁 Creando: {component_dir.relative_to(base_path)}/")

    # Generar __meta__.py
    meta_content = _generate_meta(name, component_type, domain, minimal)
    (component_dir / "__meta__.py").write_text(meta_content, encoding="utf-8")
    console.print("   ✅ __meta__.py")

    if not minimal:
        # Estructura completa
        (component_dir / "__init__.py").write_text(
            f'"""Módulo ERP Nexus: {name}"""\n'
            f'from sdk.contracts import ModuleContract\n\n'
            f'__version__ = "0.1.0"\n',
            encoding="utf-8",
        )
        console.print("   ✅ __init__.py")

        # Core
        core_dir = component_dir / "core"
        core_dir.mkdir()
        (core_dir / "__init__.py").write_text("", encoding="utf-8")
        (core_dir / "models.py").write_text(
            "# Modelos Django para este módulo\n"
            "# from django.db import models\n\n"
            "# class MiModelo(models.Model):\n"
            "#     nombre = models.CharField(max_length=100)\n",
            encoding="utf-8",
        )
        console.print("   ✅ core/models.py")

        # Events
        events_dir = component_dir / "events"
        events_dir.mkdir()
        (events_dir / "__init__.py").write_text("", encoding="utf-8")
        (events_dir / "handlers.py").write_text(
            "# Handlers de eventos para este módulo\n"
            "# Estos handlers se registran en el Event Bus del ERP\n\n"
            "# def handle_event(payload: dict) -> None:\n"
            "#     pass\n",
            encoding="utf-8",
        )
        console.print("   ✅ events/handlers.py")

        # Tests
        tests_dir = component_dir / "tests"
        tests_dir.mkdir()
        (tests_dir / "__init__.py").write_text("", encoding="utf-8")
        (tests_dir / "test_meta.py").write_text(
            f'"""Tests básicos para {name}"""\n'
            f'from pathlib import Path\n'
            f'from sdk import ComponentValidator\n\n\n'
            f'def test_meta_is_valid():\n'
            f'    """Verifica que __meta__.py es válido."""\n'
            f'    validator = ComponentValidator()\n'
            f'    meta = validator.validate_component(Path(__file__).parent.parent)\n'
            f'    assert meta.technical_name == "{name}"\n',
            encoding="utf-8",
        )
        console.print("   ✅ tests/test_meta.py")

    # Validar inmediatamente
    validator = ComponentValidator()
    try:
        meta = validator.validate_component(component_dir)
        console.print(Panel.fit(
            f"[green]✓ Módulo creado exitosamente[/green]\n\n"
            f"[bold]Nombre:[/bold] {meta.technical_name}\n"
            f"[bold]Tipo:[/bold] {meta.component_type} ({meta.package_type})\n"
            f"[bold]Versión:[/bold] {meta.version}\n"
            f"[bold]Dominio:[/bold] {meta.domain or 'custom'}\n\n"
            f"[blue]Siguiente:[/blue] Edita __meta__.py y empieza a desarrollar",
            title="🎉 Módulo Listo",
            border_style="green",
        ))
    except (ValidationError, Exception) as e:
        console.print(Panel.fit(
            f"[yellow]⚠ Módulo creado pero con warnings:[/yellow]\n\n{e}",
            title="Advertencia",
            border_style="yellow",
        ))


def _generate_meta(name: str, component_type: str, domain: str, minimal: bool) -> str:
    """Genera el contenido de __meta__.py."""
    if minimal:
        return (
            f'technical_name = "{name}"\n'
            f'display_name = "{name.replace("_", " ").title()}"\n'
            f'component_type = "{component_type}"\n'
            f'package_type = "extension"\n'
            f'python = ">=3.11"\n'
            f'erp_version = ">=0.1.0"\n'
            f'version = "0.1.0"\n'
        )

    return f'''"""
Módulo ERP Nexus — {name}
{'=' * (len(name) + 22)}

Este archivo define la metadata de tu módulo.
NO ejecutes código aquí — solo asigna valores a las variables.

Edita SOLO los valores entre comillas.
"""

# ════════════════════════════════════════════════════════════════════
# IDENTIDAD (OBLIGATORIO)
# ════════════════════════════════════════════════════════════════════

technical_name = "{name}"
display_name = "{name.replace("_", " ").title()}"
component_type = "{component_type}"
package_type = "extension"
domain = "{domain}"


# ════════════════════════════════════════════════════════════════════
# COMPATIBILIDAD (OBLIGATORIO)
# ════════════════════════════════════════════════════════════════════

python = ">=3.11"
erp_version = ">=0.1.0"


# ════════════════════════════════════════════════════════════════════
# DISTRIBUCIÓN (OBLIGATORIO)
# ════════════════════════════════════════════════════════════════════

version = "0.1.0"
license = "MIT"
keywords = ["erp", "nexus", "{name}"]
description = "Módulo ERP Nexus para {name.replace("_", " ")}"

authors = [
    {{
        "name": "Tu Nombre",
        "role": "author",
        "email": "tu@email.com",
    }}
]


# ════════════════════════════════════════════════════════════════════
# DEPENDENCIAS (OPCIONAL)
# ════════════════════════════════════════════════════════════════════

depends = []

external_dependencies = {{
    "python": [],
    "bin": [],
}}


# ════════════════════════════════════════════════════════════════════
# COMPORTAMIENTO (OPCIONAL)
# ════════════════════════════════════════════════════════════════════

installable = True
auto_install = False

registry_flags = {{
    "models": True,
    "api": False,
    "workers": False,
    "tasks": False,
}}
'''
