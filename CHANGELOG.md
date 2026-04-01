# Changelog

All notable changes to SDK Nexus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] — 2026-04-01

### Added
- CLI entry point: `sdk-nexus create|validate|package|test|info`
- ModuleContract protocol (interface for ERP modules)
- EventProvider protocol (event-driven module communication)
- MigrationProvider protocol (modules with DB migrations)
- APIProvider protocol (modules exposing API endpoints)
- Package command: creates `.npkg` zip with SHA256 checksum and manifest
- Scaffold creates full structure: `core/`, `events/`, `tests/`
- Test runner for module tests (`sdk-nexus test`)
- 15 passing tests for parser, schemas, validator, contracts

### Changed
- SDK refocused as dev toolkit (create, validate, package, test)
- contracts.py: StorageBackend → ModuleContract + EventProvider + APIProvider
- exceptions.py: removed InstallationError, added PackagingError + ScaffoldError
- install_plan.py renamed to resolution.py (DependencyPlan → resolve_dependencies)
- __init__.py: clean API surface with only dev toolkit exports
- pyproject.toml: renamed to `sdk-nexus`, added click/rich deps
- examples: cleaned up to match new scope

### Removed
- installer.py (TransactionalInstaller → moves to erp-nexus)
- registry.py (ComponentRegistry → moves to erp-nexus)
- StorageBackend protocol (installation not SDK responsibility)
- InstallationError exception

## [1.0.0] — 2026-03-12

### Added
- Initial release with component validation
- Pydantic schemas for __meta__.py
- Dependency resolver with semver support
- Transactional installer (moved to erp-nexus in Unreleased)
- Component registry (moved to erp-nexus in Unreleased)
- Meta codegen templates
- AST-based meta parser (safe, no code execution)
- Structure and dependency validators
- Examples for all major features

[1.1.0]: https://github.com/ERPNexusGroup/sdk-nexus/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ERPNexusGroup/sdk-nexus/releases/tag/v1.0.0
