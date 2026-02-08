from pathlib import Path


class MetaWriter:

    @staticmethod
    def write_meta_file(path: Path, content: str):

        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            content,
            encoding="utf-8",
            newline="\n"
        )
