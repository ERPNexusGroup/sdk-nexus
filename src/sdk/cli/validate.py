"""
Comando: sdk-nexus validate <ruta>

Valida un módulo contra los contratos del ERP Nexus.
"""
from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..validation.component_validator import ComponentValidator
from ..exceptions import ValidationError

console = Console()


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--strict", "-s", is_flag=True,
    help="Tratar warnings como errores",
)
def validate(path: str, strict: bool):
    """
    Valida un módulo ERP Nexus.

    Verifica:
      - __meta__.py existe y es válido (AST parser seguro)
      - Estructura de directorios correcta
      - Dependencias declaradas correctamente
      - Schema Pydantic pasa todas las validaciones

    Ejemplos:

      sdk-nexus validate ./mi_modulo

      sdk-nexus validate ./mi_modulo --strict
    """
    component_path = Path(path).resolve()

    if not component_path.is_dir():
        console.print(f"[red]✗ No es un directorio: {path}[/red]")
        sys.exit(1)

    meta_path = component_path / "__meta__.py"
    if not meta_path.exists():
        console.print(f"[red]✗ No se encontró __meta__.py en {path}[/red]")
        console.print(f"[yellow]💡 Crea uno con: sdk-nexus create {component_path.name}[/yellow]")
        sys.exit(1)

    # Validar
    validator = ComponentValidator()

    warnings = []

    try:
        meta = validator.validate_component(component_path)
    except ValidationError as e:
        console.print(Panel.fit(
            f"[red]❌ INVÁLIDO[/red]\n\n{e}",
            title="Validación Fallida",
            border_style="red",
        ))
        sys.exit(1)

    # Checks adicionales en modo strict
    if strict:
        if not meta.description or len(meta.description) < 50:
            warnings.append("description muy corta (mínimo 50 caracteres recomendado)")
        if not meta.authors:
            warnings.append("sin autores definidos")
        if not meta.keywords:
            warnings.append("sin keywords para búsqueda")

    # Mostrar resultado
    if warnings and strict:
        console.print(Panel.fit(
            f"[yellow]⚠ VÁLIDO con warnings[/yellow]\n\n"
            + "\n".join(f"  • {w}" for w in warnings),
            title="Validación con Advertencias",
            border_style="yellow",
        ))
        sys.exit(1)

    # Resultado OK
    table = Table(show_header=False, box=None)
    table.add_row("[bold]Nombre técnico[/bold]", meta.technical_name)
    table.add_row("[bold]Nombre visible[/bold]", meta.display_name)
    table.add_row("[bold]Tipo[/bold]", f"{meta.component_type} ({meta.package_type})")
    table.add_row("[bold]Dominio[/bold]", meta.domain or "—")
    table.add_row("[bold]Versión[/bold]", meta.version)
    table.add_row("[bold]Python[/bold]", meta.python)
    table.add_row("[bold]ERP Version[/bold]", meta.erp_version)

    if meta.authors:
        table.add_row("[bold]Autores[/bold]", ", ".join(a.name for a in meta.authors))

    if meta.depends:
        table.add_row("[bold]Dependencias[/bold]", ", ".join(meta.depends))

    console.print(Panel.fit(
        f"[green]✅ VÁLIDO[/green]\n\n",
        title="Validación Exitosa",
        border_style="green",
    ))
    console.print(table)
    console.print(f"\n[green]✓ El módulo puede empaquetarse e instalarse[/green]")
    console.print(f"[dim]Siguiente: sdk-nexus package {path}[/dim]")
