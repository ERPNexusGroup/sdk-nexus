<div align="center">

# 🛠️ SDK Nexus

**Dev Toolkit para crear módulos compatibles con ERP Nexus**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](CHANGELOG.md)

[Instalación](#instalación) • [Uso rápido](#uso-rápido) • [Comandos](#comandos) • [Flujo](#flujo-de-desarrollo) • [Contratos](#contratos-del-módulo)

</div>

---

## ¿Qué es?

SDK Nexus es el toolkit oficial para desarrolladores que quieren crear módulos para el ecosistema **ERP Nexus**. Te permite:

- **Scaffold** un módulo nuevo con estructura completa
- **Validar** tu módulo contra los contratos del ERP
- **Empaquetar** tu módulo en `.npkg` para distribución
- **Testear** tu módulo localmente

> **Nota:** El SDK **no instala** módulos. Para instalar, usa `manage.py install_module` dentro del ERP.

## Instalación

```bash
# Con pip
pip install sdk-nexus

# Con uv
uv add sdk-nexus
```

## Uso rápido

```bash
# 1. Crear un módulo nuevo
sdk-nexus create hotel_reservations --type=module --domain=hospitality

# 2. Desarrollar (models, events, api...)
cd hotel_reservations

# 3. Validar
sdk-nexus validate ./

# 4. Testear
sdk-nexus test ./

# 5. Empaquetar
sdk-nexus package ./

# 6. Instalar en el ERP
cd /path/to/erp-nexus
manage.py install_module --package ./dist/hotel_reservations-0.1.0.npkg
```

## Comandos

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `create` | Crea un módulo con estructura base | `sdk-nexus create my_module` |
| `validate` | Valida contra contratos del ERP | `sdk-nexus validate ./my_module` |
| `package` | Empaqueta en `.npkg` para distribuir | `sdk-nexus package ./my_module` |
| `test` | Ejecuta tests del módulo | `sdk-nexus test ./my_module` |
| `info` | Muestra info del SDK | `sdk-nexus info` |

### create

```bash
sdk-nexus create <nombre> [opciones]

Opciones:
  --type      module | app          (default: module)
  --domain    accounting | hospitality | inventory | custom
  --path      Directorio donde crear (default: cwd)
  --minimal   Solo __meta__.py, sin estructura
```

Genera:
```
mi_modulo/
├── __meta__.py           # Metadata del módulo
├── __init__.py           # Paquete Python
├── core/
│   ├── __init__.py
│   └── models.py         # Modelos Django (placeholder)
├── events/
│   ├── __init__.py
│   └── handlers.py       # Event handlers (placeholder)
├── api/
│   ├── __init__.py
│   └── endpoints.py      # API endpoints (placeholder)
├── tests/
│   ├── __init__.py
│   └── test_meta.py      # Test de validación
└── migrations/           # (se crea al instalar)
```

### validate

```bash
sdk-nexus validate ./mi_modulo [--strict]
```

Verifica:
- `__meta__.py` existe y es válido (AST parser seguro, sin ejecutar código)
- Schema Pydantic pasa todas las validaciones
- Estructura de directorios correcta
- Dependencias declaradas correctamente
- En modo `--strict`: warnings como errores

### package

```bash
sdk-nexus package ./mi_modulo [--output ./releases]
```

Genera:
- `mi_modulo-0.1.0.npkg` — Paquete zip comprimido
- `mi_modulo-0.1.0.manifest.json` — SHA256 checksum + metadata

Excluye automáticamente: `__pycache__`, `.git`, `.venv`, `tests/`, `*.pyc`

### test

```bash
sdk-nexus test ./mi_modulo [--coverage]
```

Ejecuta `pytest` sobre el directorio `tests/` del módulo.

## Flujo de desarrollo

```
Desarrollador                      SDK Nexus                    ERP Nexus
─────────────                      ─────────                    ─────────

sdk-nexus create mi_modulo  ──►  Crea estructura
sdk-nexus validate ./mi_mod ──►  Valida __meta__.py
sdk-nexus test ./mi_mod    ──►  Ejecuta tests
sdk-nexus package ./mi_mod ──►  Genera .npkg
                                                              manage.py install_module ──►  Instala en ERP
                                                              manage.py module list     ──►  Verifica
                                                              manage.py migrate         ──►  DB lista
```

## Contratos del módulo

Un módulo puede implementar estos protocolos:

### ModuleContract (base)

```python
from sdk.contracts import ModuleContract

class MiModulo(ModuleContract):
    @staticmethod
    def get_meta() -> dict:
        return {"name": "mi_modulo"}

    @staticmethod
    def get_version() -> str:
        return "1.0.0"
```

### EventProvider

```python
from sdk.contracts import EventProvider

class MiModulo(EventProvider):
    @staticmethod
    def get_events() -> list[str]:
        return ["invoice.created", "invoice.paid"]

    @staticmethod
    def get_event_handlers() -> dict[str, str]:
        return {
            "payment.received": "mi_modulo.events.on_payment",
        }
```

### APIProvider

```python
from sdk.contracts import APIProvider

class MiModulo(APIProvider):
    @staticmethod
    def get_api_routes() -> list[dict]:
        return [
            {"path": "/invoices", "method": "GET"},
            {"path": "/invoices", "method": "POST"},
        ]
```

## Estructura del proyecto

```
src/sdk/
├── cli/                # CLI commands (create, validate, package, test, info)
│   ├── __init__.py     # Entry point
│   ├── create.py       # Scaffold command
│   ├── validate.py     # Validation command
│   ├── package.py      # Packaging command
│   ├── test_cmd.py     # Test runner
│   └── info.py         # SDK info
├── schemas/            # Pydantic schemas (__meta__.py validation)
│   └── meta_schema.py  # BaseMetaSchema, ModuleMetaSchema, AppMetaSchema
├── validation/         # Validators
│   ├── component_validator.py
│   ├── structure_validator.py
│   └── dependency_validator.py
├── dependency/         # Dependency resolution
│   ├── resolver.py
│   ├── version_resolver.py
│   └── resolution.py   # DependencyPlan
├── meta_codegen/       # __meta__.py generation
│   ├── template_engine.py
│   ├── meta_generator.py
│   └── meta_writer.py
├── utils/              # Utilities
│   ├── meta_parser.py  # AST-based safe parser
│   ├── file_utils.py
│   └── validation_utils.py
├── contracts.py        # Protocol interfaces
├── constants.py        # Shared constants
├── exceptions.py       # SDK exceptions
└── __init__.py         # Public API
```

## Ejemplos

Ver [`examples/`](examples/) para módulos de ejemplo:
- `accounting_basic/` — Sistema contable básico con modelos, eventos y API

## Dependencias

- Python 3.11+
- pydantic >= 2.6.0
- semantic-version >= 2.10.0
- click >= 8.1.7
- rich >= 13.7.0

## Ecosistema ERP Nexus

```
┌─────────────────────────────────────────────────┐
│  sdk-nexus  →  Dev Toolkit (este repo)          │
│  Crear, validar, empaquetar módulos             │
├─────────────────────────────────────────────────┤
│  nexus (CLI)  →  Bootstrap/Deploy               │
│  nexus init / nexus server / nexus update       │
├─────────────────────────────────────────────────┤
│  erp-nexus  →  ERP Core (Django)                │
│  manage.py install_module / module list / api   │
├─────────────────────────────────────────────────┤
│  Módulos  →  accounting, invoicing, inventory...│
│  Creados con sdk-nexus, instalados en erp-nexus │
└─────────────────────────────────────────────────┘
```

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guías de contribución, git flow y convenciones.

## Licencia

GPL-3.0-or-later — Ver [LICENSE](LICENSE)
