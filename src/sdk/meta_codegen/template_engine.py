from pathlib import Path


class TemplateEngine:

    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir

    def render(self, template_name: str, context: dict) -> str:

        template_path = self.templates_dir / template_name

        if not template_path.exists():
            raise FileNotFoundError(
                f"Template no encontrado: {template_path}"
            )

        content = template_path.read_text(encoding="utf-8")

        for key, value in context.items():
            content = content.replace(
                "{{ " + key + " }}",
                str(value)
            )

        return content
