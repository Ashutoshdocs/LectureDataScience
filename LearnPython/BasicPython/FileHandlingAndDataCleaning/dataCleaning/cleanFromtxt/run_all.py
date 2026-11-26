"""
Run all seven file-processing steps in the correct order.

Run this helper from any folder:
    python run_all.py

If any step fails, the pipeline stops and reports the failing script.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Each step consumes files produced by earlier steps.
steps = [
    "step0_reading_files.py",
    "step1_strip_spaces.py",
    "step2_remove_junk.py",
    "step3_fix_words.py",
    "step4_group_and_dedupe.py",
    "step5_to_json.py",
    "step6_answers.py",
]

for step in steps:
    script_path = BASE_DIR / step

    print("\n" + "=" * 65)
    print("RUNNING:", step)
    print("=" * 65)

    # Use the same Python interpreter that launched run_all.py.
    # check=True raises an error if a step returns a non-zero exit code.
    subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE_DIR,
        check=True,
    )

print("\nAll seven steps completed successfully.")
