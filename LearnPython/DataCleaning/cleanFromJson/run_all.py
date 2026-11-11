"""
Run the complete social-network project in the correct order.

This helper runs Task 1, Task 2, Task 3, and Task 4.
Run it from any folder with: python run_all.py
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Each task is run using the same Python interpreter as this script.
task_files = [
    "task1_clean_and_structure.py",
    "task2_people_you_may_know.py",
    "task3_pages_you_might_like.py",
    "task4_combine_recommendations.py",
]

for task_file in task_files:
    script_path = BASE_DIR / task_file
    print(f"\n{'=' * 60}")
    print(f"RUNNING: {task_file}")
    print("=" * 60)

    # check=True stops the pipeline if a task fails.
    subprocess.run([sys.executable, str(script_path)], check=True)

print("\nAll social-network tasks completed successfully.")
