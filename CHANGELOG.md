# Changelog

All notable changes to SDK Nexus will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased] — dev branch

### Changed
- Refocus SDK as dev toolkit (create, validate, package, test)
- Removed installer/registry responsibilities (now in erp-nexus)
- Updated README with new scope and usage

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

[Unreleased]: https://github.com/ERPNexusGroup/sdk-nexus/compare/v1.0.0...dev
[1.0.0]: https://github.com/ERPNexusGroup/sdk-nexus/releases/tag/v1.0.0
