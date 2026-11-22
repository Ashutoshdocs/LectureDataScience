"""Run every lecture.py in order and report which ones succeeded.

Usage:  python run_all.py
"""
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).parent
scripts = sorted(root.glob("*/lecture.py"))

failed = []
for script in scripts:
    print("=" * 70)
    print(f"RUNNING {script.relative_to(root)}")
    print("=" * 70)
    result = subprocess.run([sys.executable, script.name], cwd=script.parent)
    if result.returncode != 0:
        failed.append(script)

print("\n" + "=" * 70)
print(f"{len(scripts) - len(failed)} of {len(scripts)} scripts ran successfully")
for f in failed:
    print("  FAILED:", f.relative_to(root))
