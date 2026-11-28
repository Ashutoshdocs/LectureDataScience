from pathlib import Path
import tempfile


def process_text_in_temporary_workspace(source_text: str) -> str:
    """
    Write source text into a temporary file, read it back, and return
    a processed result. The temporary directory is removed after the block.
    """
    with tempfile.TemporaryDirectory(prefix="python_processing_") as temp_dir:
        workspace = Path(temp_dir)
        temporary_input = workspace / "intermediate_input.txt"
        temporary_output = workspace / "intermediate_output.txt"

        temporary_input.write_text(source_text, encoding="utf-8")

        original_text = temporary_input.read_text(encoding="utf-8")
        processed_text = original_text.upper()

        temporary_output.write_text(processed_text, encoding="utf-8")
        result = temporary_output.read_text(encoding="utf-8")

        print("Temporary workspace:", workspace)
        print("Temporary input exists:", temporary_input.exists())
        print("Temporary output exists:", temporary_output.exists())

        return result
