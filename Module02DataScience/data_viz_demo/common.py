"""
common.py
---------
Shared code used by every demo script in this project.

It provides:
  1. Sample datasets (generated in code, so no internet or CSV files needed)
  2. A consistent plot style
  3. A helper to save + show figures in one call

Every topic file does:  from common import ...
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Folder where all generated charts are saved
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fixed seed -> same "random" data every run, so results are reproducible
SEED = 42

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def apply_style():
    """Apply one consistent look to all Matplotlib charts."""
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.rcParams.update({
        "figure.figsize": (9, 5.5),
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "legend.fontsize": 10,
    })


def get_monthly_sales():
    """
    Monthly sales (in thousands) for three product categories.
    Columns: Month, Electronics, Clothing, Groceries
    """
    RNG = np.random.default_rng(SEED)
    base = np.linspace(40, 70, 12)
    return pd.DataFrame({
        "Month": MONTHS,
        "Electronics": (base + RNG.normal(0, 5, 12)).round(1),
        "Clothing": (base * 0.7 + 10 * np.sin(np.arange(12) / 2) + RNG.normal(0, 3, 12)).round(1),
        "Groceries": (np.full(12, 45) + RNG.normal(0, 2, 12)).round(1),
    })


def get_students(n=200):
    """
    A student dataset for distributions and relationships.
    Columns: study_hours, sleep_hours, score, gender, grade_level
    """
    RNG = np.random.default_rng(SEED)
    study = RNG.uniform(0, 10, n).round(1)
    sleep = RNG.normal(7, 1.2, n).clip(4, 10).round(1)
    score = (35 + 5 * study + 2 * (sleep - 7) + RNG.normal(0, 7, n)).clip(0, 100).round(0)
    return pd.DataFrame({
        "study_hours": study,
        "sleep_hours": sleep,
        "score": score,
        "gender": RNG.choice(["Male", "Female"], n),
        "grade_level": RNG.choice(["Freshman", "Sophomore", "Junior", "Senior"], n),
    })


def get_market_share():
    """Market share (%) of smartphone brands - good for pie charts."""
    return {"Brand A": 32, "Brand B": 25, "Brand C": 18, "Brand D": 12, "Others": 13}


def save_and_show(fig, filename, show=True):
    """Save a figure into output/ and optionally display it."""
    path = os.path.join(OUTPUT_DIR, filename)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    print(f"[saved] {path}")
    if show:
        plt.show()
    plt.close(fig)
