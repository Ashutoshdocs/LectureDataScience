import logging
from datetime import datetime
from pathlib import Path

from temp_operations import process_text_in_temporary_workspace

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "input" / "source.txt"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"


def configure_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_DIR / "processing.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    configure_logging()

    if not INPUT_FILE.is_file():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    source_text = INPUT_FILE.read_text(encoding="utf-8")
    processed_text = process_text_in_temporary_workspace(source_text)

    # Save the final result outside the temporary directory.
    final_output = OUTPUT_DIR / "processed_result.txt"
    final_output.write_text(processed_text, encoding="utf-8")

    logging.info("Processed input file %s", INPUT_FILE)
    logging.info("Saved permanent output to %s", final_output)

    print("\nFinal result saved to:", final_output)
    print("Completed at:", datetime.now().isoformat(timespec="seconds"))
    print("The temporary workspace has been cleaned up after processing.")


if __name__ == "__main__":
    main()
