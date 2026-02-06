from semantic_version import Version, SimpleSpec # type: ignore

class VersionUtils:
    """Utilidades para manejo de versiones semánticas."""

    @staticmethod
    def is_compatible(version: str, spec: str) -> bool:
        """Verifica si una versión cumple con una especificación."""
        try:
            v = Version(version)
            s = SimpleSpec(spec)
            return s.match(v)
        except ValueError:
            return False
