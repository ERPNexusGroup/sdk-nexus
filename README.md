# SDK Nexus — Dev Toolkit para ERP Nexus

Toolkit para desarrolladores que quieren crear módulos compatibles con el ecosistema ERP Nexus.

## ¿Qué es?

SDK Nexus te permite:
- **Scaffold** un módulo nuevo desde cero
- **Validar** tu módulo contra los contratos del ERP
- **Empaquetar** tu módulo para distribución
- **Testear** tu módulo localmente antes de instalar

No instala módulos — eso lo hace el ERP (`manage.py install_module`).

## Instalación

```bash
uv add sdk-nexus
# o
pip install sdk-nexus
```

## Uso rápido

```bash
# Crear un módulo nuevo
sdk-nexus create hotel_reservations --type=module

# Validar un módulo existente
sdk-nexus validate ./hotel_reservations

# Empaquetar para distribución
sdk-nexus package ./hotel_reservations

# Ejecutar tests del módulo
sdk-nexus test ./hotel_reservations
```

## Flujo de desarrollo

```
1. sdk-nexus create mi_modulo     → Estructura base + __meta__.py
2. (desarrollar: models, views, events...)
3. sdk-nexus validate ./mi_modulo → Verifica contra contratos del ERP
4. sdk-nexus test ./mi_modulo     → Tests del módulo
5. sdk-nexus package ./mi_modulo  → Genera .npkg para distribuir
6. Subir a git o compartir .npkg
```

## Estructura del proyecto

```
src/sdk/
├── schemas/          # Pydantic schemas (__meta__.py validation)
├── validation/       # Validators de estructura y dependencias
├── dependency/       # Resolución de dependencias (semver)
├── meta_codegen/     # Generación de __meta__.py templates
├── utils/            # Utilidades (meta_parser, file_utils, etc.)
├── contracts.py      # Interfaces/protocolos para el ERP
├── constants.py      # Constantes del ecosistema
├── validator.py      # Validador principal
└── __init__.py       # API pública
```

## Documentación

- [Especificación de módulos](docs/SPECIFICATION.md)
- [Convenciones de nombres](docs/NAMING_CONVENTIONS.md)
- [Palabras clave](docs/KEYWORDS.md)
- [Ejemplos](docs/EXAMPLES.md)

## Licencia

GPL-3.0-or-later
