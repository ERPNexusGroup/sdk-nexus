"""
Comando: sdk-nexus info

Muestra información sobre el SDK y su entorno.
"""
from __future__ import annotations

import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .. import __version__
from ..constants import META_SCHEMA_VERSION, DEFAULT_PYTHON, DEFAULT_ERP_VERSION

console = Console()


@click.command()
def info():
    """Muestra información del SDK y su configuración."""
    table = Table(show_header=False, box=None)
    table.add_row("[bold]SDK Version[/bold]", __version__)
    table.add_row("[bold]Meta Schema[/bold]", META_SCHEMA_VERSION)
    table.add_row("[bold]Python mínimo[/bold]", DEFAULT_PYTHON)
    table.add_row("[bold]ERP mínimo[/bold]", DEFAULT_ERP_VERSION)
    table.add_row("[bold]Python actual[/bold]", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

    console.print(Panel.fit(
        table,
        title="🛠️  SDK Nexus — Info",
        border_style="cyan",
    ))

    console.print("\n[bold]Comandos disponibles:[/bold]")
    console.print("  [green]sdk-nexus create[/green] <nombre>   Crear módulo nuevo")
    console.print("  [green]sdk-nexus validate[/green] <ruta>    Validar módulo")
    console.print("  [green]sdk-nexus package[/green] <ruta>     Empaquetar módulo")
    console.print("  [green]sdk-nexus test[/green] <ruta>        Ejecutar tests")
