"""Tests para el SDK Nexus — validación, schemas y CLI."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from sdk import ComponentValidator, BaseMetaSchema, __version__
from sdk.exceptions import ValidationError
from sdk.utils.meta_parser import parse_meta_file


def _create_module(tmp_path: Path, name: str = "test_module", **overrides) -> Path:
    """Helper: crea un directorio de módulo válido con __meta__.py."""
    defaults = {
        "display_name": name.replace("_", " ").title(),
        "component_type": "module",
        "package_type": "extension",
        "python": ">=3.11",
        "erp_version": ">=0.1.0",
        "version": "0.1.0",
    }
    defaults.update(overrides)

    mod_dir = tmp_path / name
    mod_dir.mkdir()

    lines = [f'technical_name = "{name}"']
    for k, v in defaults.items():
        if isinstance(v, list):
            lines.append(f"{k} = {v}")
        elif isinstance(v, bool):
            lines.append(f"{k} = {str(v)}")
        else:
            lines.append(f'{k} = "{v}"')

    (mod_dir / "__meta__.py").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (mod_dir / "__init__.py").write_text("")
    return mod_dir


class TestMetaParser:
    def test_parse_valid_meta(self, tmp_path):
        mod_dir = _create_module(tmp_path, name="hello_world")
        data = parse_meta_file(mod_dir / "__meta__.py")
        assert data["technical_name"] == "hello_world"
        assert data["component_type"] == "module"

    def test_parse_missing_file(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            parse_meta_file(tmp_path / "no_existe.py")

    def test_ignores_import_statements(self, tmp_path):
        """Import statements son ignorados por el AST parser (no extrae, no ejecuta)."""
        mod_dir = tmp_path / "import_test"
        mod_dir.mkdir()
        meta = mod_dir / "__meta__.py"
        meta.write_text('import os\ntechnical_name = "import_test"\n')
        data = parse_meta_file(meta)
        # El parser solo extrae assignments, import es ignorado
        assert data["technical_name"] == "import_test"
        assert "os" not in data  # import no se extrae como variable


class TestSchemaValidation:
    def test_valid_module(self):
        schema = BaseMetaSchema(
            technical_name="my_module",
            display_name="My Module",
            component_type="module",
            package_type="extension",
            version="1.0.0",
        )
        assert schema.technical_name == "my_module"
        assert schema.version == "1.0.0"

    def test_invalid_name(self):
        with pytest.raises(Exception):
            BaseMetaSchema(
                technical_name="Bad-Name",
                display_name="Bad",
                component_type="module",
                package_type="extension",
                version="1.0.0",
            )

    def test_invalid_version(self):
        with pytest.raises(Exception):
            BaseMetaSchema(
                technical_name="my_module",
                display_name="My Module",
                component_type="module",
                package_type="extension",
                version="not-semver",
            )


class TestComponentValidator:
    def test_valid_component(self, tmp_path):
        """El directorio del módulo debe llamarse igual que technical_name."""
        mod_dir = _create_module(tmp_path, name="valid_mod")

        validator = ComponentValidator()
        meta = validator.validate_component(mod_dir)
        assert meta.technical_name == "valid_mod"

    def test_missing_meta_file(self, tmp_path):
        mod_dir = tmp_path / "empty"
        mod_dir.mkdir()

        validator = ComponentValidator()
        with pytest.raises(Exception):
            validator.validate_component(mod_dir)

    def test_validate_manifest_alias(self, tmp_path):
        """validate_manifest es alias de validate_component."""
        mod_dir = _create_module(tmp_path, name="alias_test")
        validator = ComponentValidator()
        meta = validator.validate_manifest(mod_dir)
        assert meta.technical_name == "alias_test"

    def test_name_mismatch(self, tmp_path):
        """Directorio y technical_name deben coincidir."""
        mod_dir = _create_module(tmp_path, name="real_name")
        # Cambiar el technical_name en __meta__.py para que no coincida
        meta_file = mod_dir / "__meta__.py"
        content = meta_file.read_text()
        meta_file.write_text(content.replace("real_name", "different_name"))

        validator = ComponentValidator()
        with pytest.raises(ValidationError):
            validator.validate_component(mod_dir)


class TestContracts:
    def test_module_contract_protocol(self):
        from sdk.contracts import ModuleContract

        class MyModule:
            @staticmethod
            def get_meta():
                return {"name": "test"}

            @staticmethod
            def get_version():
                return "1.0.0"

        assert isinstance(MyModule(), ModuleContract)

    def test_event_provider_protocol(self):
        from sdk.contracts import EventProvider

        class MyEvents:
            @staticmethod
            def get_events():
                return ["invoice.created"]

            @staticmethod
            def get_event_handlers():
                return {"invoice.created": "my_mod.handlers.on_invoice"}

        assert isinstance(MyEvents(), EventProvider)

    def test_api_provider_protocol(self):
        from sdk.contracts import APIProvider

        class MyAPI:
            @staticmethod
            def get_api_routes():
                return [{"path": "/invoices", "method": "GET"}]

        assert isinstance(MyAPI(), APIProvider)


class TestVersion:
    def test_version_is_string(self):
        assert isinstance(__version__, str)

    def test_version_is_semver(self):
        from semantic_version import Version
        Version(__version__)  # Should not raise
