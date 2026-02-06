import shutil
from pathlib import Path
from typing import Union

class FileUtils:
    """Utilidades para manejo de archivos."""

    @staticmethod
    def copy_tree(src: Union[str, Path], dst: Union[str, Path]) -> None:
        """Copia un directorio recursivamente."""
        src = Path(src)
        dst = Path(dst)
        if not src.exists():
            raise FileNotFoundError(f"Origen no encontrado: {src}")
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)

    @staticmethod
    def remove_tree(path: Union[str, Path]) -> None:
        """Elimina un directorio recursivamente."""
        path = Path(path)
        if path.exists() and path.is_dir():
            shutil.rmtree(path)
