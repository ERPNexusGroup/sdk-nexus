import pytest
from pydantic import ValidationError
from src.sdk.schemas import ModuleSchema, AppSchema, LibSchema

def test_module_schema_valid():
    data = {
        "name": "mod_sales",
        "version": "1.0.0",
        "description": "Sales module",
        "author": "Me",
        "email": "me@example.com"
    }
    schema = ModuleSchema(**data)
    assert schema.name == "mod_sales"

def test_module_schema_invalid_version():
    data = {
        "name": "mod_sales",
        "version": "invalid",
        "description": "Sales module",
        "author": "Me",
        "email": "me@example.com"
    }
    with pytest.raises(ValidationError):
        ModuleSchema(**data)

def test_app_schema_valid():
    data = {
        "name": "app_pos",
        "version": "2.0.0",
        "description": "POS App",
        "parent_module": "mod_sales"
    }
    schema = AppSchema(**data)
    assert schema.name == "app_pos"

def test_lib_schema_valid():
    data = {
        "name": "lib_utils",
        "version": "0.5.0",
        "description": "Utils lib"
    }
    schema = LibSchema(**data)
    assert schema.name == "lib_utils"
