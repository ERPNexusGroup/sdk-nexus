"""
Comando: sdk-nexus package <ruta>

Empaqueta un módulo en un archivo .npkg (zip) para distribución.
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from ..validation.component_validator import ComponentValidator
from ..exceptions import PackagingError, ValidationError
from ..utils.meta_parser import parse_meta_file

console = Console()

# Archivos/carpetas a excluir del paquete
EXCLUDE_PATTERNS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".git",
    ".gitignore",
    ".venv",
    "venv",
    ".env",
    "*.pyc",
    ".idea",
    ".vscode",
    "node_modules",
    "*.egg-info",
    "dist",
    "build",
}


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--output", "-o", default=None,
    help="Directorio de salida (default: ./dist)",
)
@click.option(
    "--skip-validation", is_flag=True,
    help="Omitir validación (no recomendado)",
)
def package(path: str, output: str | None, skip_validation: bool):
    """
    Empaqueta un módulo en un archivo .npkg para distribución.

    El paquete incluye:
      - Todos los archivos del módulo (excepto tests, caches, etc.)
      - SHA256 checksum para verificación de integridad
      - Manifest JSON con metadata del paquete

    Ejemplos:

      sdk-nexus package ./mi_modulo

      sdk-nexus package ./mi_modulo --output ./releases
    """
    component_path = Path(path).resolve()

    if not component_path.is_dir():
        console.print(f"[red]✗ No es un directorio: {path}[/red]")
        sys.exit(1)

    # Validar antes de empaquetar
    if not skip_validation:
        console.print("🔍 Validando módulo...")
        validator = ComponentValidator()
        try:
            meta = validator.validate_component(component_path)
        except ValidationError as e:
            console.print(f"[red]✗ Validación fallida: {e}[/red]")
            console.print("[yellow]Usa --skip-validation para forzar[/yellow]")
            sys.exit(1)
    else:
        meta_data = parse_meta_file(component_path / "__meta__.py")
        meta = type("Meta", (), meta_data)()

    # Determinar nombre y versión
    name = meta.technical_name if hasattr(meta, "technical_name") else component_path.name
    version = meta.version if hasattr(meta, "version") else "0.0.0"
    package_name = f"{name}-{version}.npkg"

    # Directorio de salida
    output_dir = Path(output) if output else Path.cwd() / "dist"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / package_name

    # Crear paquete zip
    console.print(f"📦 Empaquetando: {name} v{version}")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        files_added = 0

        for item in sorted(component_path.rglob("*")):
            # Excluir patrones
            rel = item.relative_to(component_path)
            parts = rel.parts

            if any(
                part.startswith(".") or part in EXCLUDE_PATTERNS or part.endswith(".pyc")
                for part in parts
            ):
                continue

            if item.is_file():
                arcname = f"{name}/{rel}"
                zf.write(item, arcname)
                files_added += 1

    # Calcular checksum
    sha256 = hashlib.sha256(output_path.read_bytes()).hexdigest()

    # Generar manifest
    manifest = {
        "name": name,
        "version": version,
        "package_format": "npkg-1.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "files": files_added,
        "sha256": sha256,
    }
    manifest_path = output_dir / f"{name}-{version}.manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    # Resultado
    size_kb = output_path.stat().st_size / 1024
    console.print(Panel.fit(
        f"[green]✓ Paquete creado[/green]\n\n"
        f"[bold]Archivo:[/bold] {output_path}\n"
        f"[bold]Tamaño:[/bold] {size_kb:.1f} KB\n"
        f"[bold]Archivos:[/bold] {files_added}\n"
        f"[bold]SHA256:[/bold] {sha256[:16]}...\n\n"
        f"[dim]Manifest: {manifest_path}[/dim]",
        title="📦 Paquete Listo",
        border_style="green",
    ))
    console.print(f"\n[blue]Para instalar en el ERP:[/blue]")
    console.print(f"  manage.py install_module --package {output_path}")
