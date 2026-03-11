import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from sdk.installer import TransactionalInstaller  # noqa: E402
from sdk.registry import ComponentRegistry  # noqa: E402
from sdk.contracts import StorageBackend  # noqa: E402
from sdk.exceptions import InstallationError  # noqa: E402


def _write_meta(component_dir: Path, *, name: str, depends: list | None = None) -> None:
    depends = depends or []
    content = (
        f'technical_name = "{name}"\n'
        f'display_name = "{name.replace("_", " ").title()}"\n'
        'component_type = "module"\n'
        'package_type = "extension"\n'
        'python = ">=3.11"\n'
        'erp_version = ">=0.1.0"\n'
        'version = "0.1.0"\n'
        f"depends = {depends}\n"
    )
    (component_dir / "__meta__.py").write_text(content, encoding="utf-8")


class FilesystemStorage(StorageBackend):
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.registry = ComponentRegistry(self.base_path / "registry.json")

    def copy_files(self, source: Path, destination: Path) -> None:
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)

    def remove_files(self, path: Path) -> None:
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()

    def register_component(self, path: Path, manifest: dict) -> None:
        self.registry.register(manifest["technical_name"], {"path": str(path)})

    def unregister_component(self, name: str) -> None:
        self.registry.unregister(name)

    def resolve_dependency(self, name: str, version_spec: str):
        return None

    def get_default_install_path(self, component_name: str) -> Path:
        return self.base_path / component_name


def test_install_success(tmp_path: Path) -> None:
    component_dir = tmp_path / "demo_module"
    component_dir.mkdir()
    _write_meta(component_dir, name="demo_module")

    storage = FilesystemStorage(tmp_path / "installed")
    installer = TransactionalInstaller(storage)

    result = installer.install(component_dir)

    assert result.name == "demo_module"
    assert (storage.base_path / "demo_module").exists()
    assert storage.registry.get("demo_module") is not None


def test_install_rollback_on_register_failure(tmp_path: Path) -> None:
    component_dir = tmp_path / "bad_module"
    component_dir.mkdir()
    _write_meta(component_dir, name="bad_module")

    class FailingStorage(FilesystemStorage):
        def register_component(self, path: Path, manifest: dict) -> None:
            raise RuntimeError("registry down")

    storage = FailingStorage(tmp_path / "installed")
    installer = TransactionalInstaller(storage)

    with pytest.raises(InstallationError):
        installer.install(component_dir)

    assert not (storage.base_path / "bad_module").exists()
    assert storage.registry.get("bad_module") is None


def test_install_many_respects_dependencies(tmp_path: Path) -> None:
    base = tmp_path / "components"
    base.mkdir()

    comp_a = base / "core_auth"
    comp_b = base / "core_users"
    comp_a.mkdir()
    comp_b.mkdir()

    _write_meta(comp_a, name="core_auth")
    _write_meta(comp_b, name="core_users", depends=["core_auth"])

    storage = FilesystemStorage(tmp_path / "installed")
    installer = TransactionalInstaller(storage)

    results = installer.install_many([comp_b, comp_a])

    assert [r.name for r in results] == ["core_auth", "core_users"]
