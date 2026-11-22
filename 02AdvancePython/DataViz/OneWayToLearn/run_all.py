"""
run_all.py
----------
Runs every lecture's lecture.py in order (no chart windows) and reports which ones succeeded.
Each lecture saves its charts into its own output/ folder.

Usage:  python run_all.py
"""
import os
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parent
scripts = sorted(root.glob("[0-9][0-9]_*/lecture.py"))
env = {**os.environ, "MPLBACKEND": "Agg"}          # no GUI windows; plt.show() becomes a no-op

failed = []
for script in scripts:
    print("=" * 70)
    print(f"RUNNING {script.relative_to(root)}")
    print("=" * 70)
    if subprocess.run([sys.executable, script.name], cwd=script.parent, env=env).returncode != 0:
        failed.append(script)

charts = sorted(root.glob("[0-9][0-9]_*/output/*.png"))
print("\n" + "=" * 70)
print(f"{len(scripts) - len(failed)} of {len(scripts)} scripts ran successfully, {len(charts)} charts saved")
for f in failed:
    print("  FAILED:", f.relative_to(root))
