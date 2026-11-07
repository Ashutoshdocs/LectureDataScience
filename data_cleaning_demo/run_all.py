"""Run every step in order:  python run_all.py"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STEPS = [
    "step0_reading_csv", "step1_remove_duplicates", "step2_clean_text",
    "step3_fix_numbers", "step4_parse_dates", "step5_emails_booleans",
    "step6_missing_values", "step7_structure", "step8_summary",
]

for step in STEPS:
    print(f"\n\n######## RUNNING {step}.py ########")
    result = subprocess.run([sys.executable, str(HERE / f"{step}.py")], cwd=HERE)
    if result.returncode != 0:
        sys.exit(f"Stopped: {step}.py failed.")
print("\nAll steps finished. Clean data: output/cleaned_data.csv")
