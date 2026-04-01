# Contributing to SDK Nexus

## Git Flow

We use [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/):

```
main        ← Producción (stable releases)
  └── dev   ← Integración (trabajo activo)
        ├── feature/create-command
        ├── feature/package-command
        └── fix/validator-edge-case
```

### Rules

1. **Nunca commit directo a `main`** — solo merges desde `dev` con PR aprobado
2. **Trabaja en `dev` o en branches `feature/*`** desde `dev`
3. **PRs a `dev`** requieren review antes de merge
4. **Releases**: `dev` → PR → `main` con tag semver (v1.1.0)

### Branch naming

- `feature/description` — nueva funcionalidad
- `fix/description` — corrección de bug
- `refactor/description` — refactorización
- `docs/description` — documentación

### Commits

Usa [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add scaffold command for module creation
fix: handle empty __meta__.py gracefully
refactor: separate validator from installer
docs: update SPECIFICATION with event contracts
test: add tests for dependency resolver
```

## Development setup

```bash
# Clone
git clone https://github.com/ERPNexusGroup/sdk-nexus.git
cd sdk-nexus
git checkout dev

# Install dependencies
uv sync

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src/sdk
```

## Pull Request checklist

- [ ] Tests pasan (`uv run pytest`)
- [ ] Sin errores de tipo (`uv run mypy src`)
- [ ] CHANGELOG.md actualizado
- [ ] Convención de commits seguida
- [ ] Documentación actualizada si aplica
