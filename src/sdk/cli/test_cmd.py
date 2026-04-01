"""
Comando: sdk-nexus test <ruta>

Ejecuta los tests de un módulo ERP Nexus.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

console = Console()


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--verbose", "-v", is_flag=True,
    help="Salida detallada",
)
@click.option(
    "--coverage", "-c", is_flag=True,
    help="Incluir reporte de cobertura",
)
def test(path: str, verbose: bool, coverage: bool):
    """
    Ejecuta los tests de un módulo ERP Nexus.

    Busca el directorio tests/ dentro del módulo y ejecuta pytest.
    El módulo debe tener tests/test_meta.py como mínimo.

    Ejemplos:

      sdk-nexus test ./mi_modulo

      sdk-nexus test ./mi_modulo --coverage
    """
    component_path = Path(path).resolve()
    tests_dir = component_path / "tests"

    if not tests_dir.exists():
        console.print(f"[yellow]⚠ No hay directorio tests/ en {path}[/yellow]")
        console.print(f"[dim]Crea tests con: sdk-nexus create {component_path.name}[/dim]")
        sys.exit(1)

    test_files = list(tests_dir.glob("test_*.py"))
    if not test_files:
        console.print(f"[yellow]⚠ No se encontraron archivos test_*.py en {tests_dir}[/yellow]")
        sys.exit(1)

    console.print(f"🧪 Ejecutando tests: {component_path.name}")
    console.print(f"   Encontrados: {len(test_files)} archivo(s) de test\n")

    # Construir comando pytest
    cmd = [sys.executable, "-m", "pytest", str(tests_dir)]

    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")

    if coverage:
        cmd = [
            sys.executable, "-m", "pytest",
            str(tests_dir),
            f"--cov={component_path}",
            "--cov-report=term-missing",
        ]

    # Ejecutar
    result = subprocess.run(cmd, cwd=str(component_path))

    if result.returncode == 0:
        console.print(Panel.fit(
            "[green]✓ Todos los tests pasaron[/green]",
            title="✅ Tests OK",
            border_style="green",
        ))
    else:
        console.print(Panel.fit(
            "[red]✗ Algunos tests fallaron[/red]",
            title="❌ Tests Fallidos",
            border_style="red",
        ))
        sys.exit(1)
