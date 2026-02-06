import ast
from pathlib import Path
from typing import List

class ValidationUtils:
    """Utilidades de validación estática."""

    @staticmethod
    def validate_python_syntax(file_path: Path) -> bool:
        """Valida la sintaxis de un archivo Python sin ejecutarlo."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source)
            return True
        except (SyntaxError, UnicodeDecodeError):
            return False

    @staticmethod
    def scan_directory_for_syntax_errors(directory: Path) -> List[Path]:
        """Escanea un directorio buscando archivos Python con errores de sintaxis."""
        errors = []
        for file_path in directory.rglob("*.py"):
            if not ValidationUtils.validate_python_syntax(file_path):
                errors.append(file_path)
        return errors
