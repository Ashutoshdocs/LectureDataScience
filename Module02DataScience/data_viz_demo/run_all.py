"""
run_all.py
----------
Runs every demo script in order and saves all charts to output/
without opening windows (useful for a quick check).

Usage:  python run_all.py
"""

import glob
import os
import runpy
import matplotlib

matplotlib.use("Agg")  # no GUI windows; plt.show() becomes a no-op

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)

for script in sorted(glob.glob("[0-9][0-9]_*.py")):
    print(f"\n=== Running {script} ===")
    runpy.run_path(script, run_name="__main__")

print("\nDone. Open the output/ folder to see all charts.")
