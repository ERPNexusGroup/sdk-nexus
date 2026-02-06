import pytest
from pathlib import Path
import json
from src.sdk.validator import ComponentValidator
from src.sdk.exceptions import ValidationError

@pytest.fixture
def valid_module_path(tmp_path):
    d = tmp_path / "mod_test"
    d.mkdir()
    manifest = {
        "name": "mod_test",
        "version": "1.0.0",
        "description": "Test module",
        "author": "Test",
        "email": "test@example.com"
    }
    with open(d / "module.json", "w") as f:
        json.dump(manifest, f)
    return d / "module.json"

def test_validate_valid_module(valid_module_path):
    validator = ComponentValidator()
    schema = validator.validate_manifest(valid_module_path)
    assert schema.name == "mod_test"
    assert schema.version == "1.0.0"

def test_validate_invalid_name(tmp_path):
    d = tmp_path / "invalid_mod"
    d.mkdir()
    manifest = {
        "name": "invalid_name",
        "version": "1.0.0",
        "description": "Invalid module",
        "author": "Test",
        "email": "test@example.com"
    }
    p = d / "module.json"
    with open(p, "w") as f:
        json.dump(manifest, f)

    validator = ComponentValidator()
    with pytest.raises(ValidationError):
        validator.validate_manifest(p)
