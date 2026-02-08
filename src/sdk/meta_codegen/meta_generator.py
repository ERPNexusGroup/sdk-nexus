from pathlib import Path
from .template_engine import TemplateEngine
from .meta_writer import MetaWriter
from ..constants import (
    DEFAULT_PYTHON,
    DEFAULT_ERP_VERSION,
    META_SCHEMA_VERSION,
    META_TEMPLATE_VERSION,
)
from ..schemas.meta_schema import BaseMetaSchema


class MetaGenerator:

    def __init__(self, templates_dir: Path):
        self.engine = TemplateEngine(templates_dir)

    def build_context(self, data: dict) -> dict:

        validated = BaseMetaSchema(**data)
        data = validated.model_dump()

        context = {
            "meta_schema_version": META_SCHEMA_VERSION,
            "meta_template_version": META_TEMPLATE_VERSION,
            "technical_name": data["technical_name"],
            "display_name": data["display_name"],
            "component_type": data["component_type"],
            "package_type": data["package_type"],
            "domain": data.get("domain", "custom"),
            "python": data.get("python", DEFAULT_PYTHON),
            "erp_version": data.get("erp_version", DEFAULT_ERP_VERSION),
            "version": data["version"],
            "description": data.get(
                "description",
                f"Componente ERP NEXUS para {data['technical_name']}"
            ),
        }

        return context

    def generate(self, data: dict) -> str:

        context = self.build_context(data)

        return self.engine.render(
            "meta_v2.py.tpl",
            context
        )

    def generate_and_write(
        self,
        output_path: Path,
        data: dict
    ):

        content = self.generate(data)

        MetaWriter.write_meta_file(
            output_path,
            content
        )
