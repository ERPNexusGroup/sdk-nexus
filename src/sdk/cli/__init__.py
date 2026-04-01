"""
CLI del SDK Nexus.

Comandos disponibles:
  sdk-nexus create   — Crea un módulo nuevo con estructura base
  sdk-nexus validate — Valida un módulo contra los contratos del ERP
  sdk-nexus package  — Empaqueta un módulo para distribución
  sdk-nexus test     — Ejecuta tests de un módulo
  sdk-nexus info     — Muestra información del SDK
"""
import click
from .create import create
from .validate import validate
from .package import package
from .test_cmd import test
from .info import info


@click.group()
@click.version_option(package_name="sdk-nexus", prog_name="sdk-nexus")
def cli():
    """
    🛠️  sdk-nexus — Dev Toolkit para ERP Nexus

    Crea, valida, empaqueta y testea módulos para el ecosistema ERP Nexus.
    """


cli.add_command(create)
cli.add_command(validate)
cli.add_command(package)
cli.add_command(test)
cli.add_command(info)


if __name__ == "__main__":
    cli()
