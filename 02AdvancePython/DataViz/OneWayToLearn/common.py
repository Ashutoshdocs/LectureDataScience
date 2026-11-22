"""
common.py
---------
Shared code used by every lecture in this course.

It provides:
  1. Sample datasets, generated in code (no internet or CSV files needed, same numbers every run)
  2. One consistent Matplotlib style
  3. save_and_show(): saves a figure into the CALLING lecture's own output/ folder, then shows it

Every lecture starts with:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))   # make common.py importable
    from common import ...
"""

import os
import pathlib
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

SEED = 42                      # fixed seed -> the same "random" data every run
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
CATEGORIES = ["Electronics", "Clothing", "Groceries"]


# ----------------------------------------------------------------------------- style
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


# ----------------------------------------------------------------------------- datasets
def get_monthly_sales():
    """Monthly sales (in thousands) for three product categories.
    Columns: Month, Electronics, Clothing, Groceries"""
    rng = np.random.default_rng(SEED)
    base = np.linspace(40, 70, 12)
    return pd.DataFrame({
        "Month": MONTHS,
        "Electronics": (base + rng.normal(0, 5, 12)).round(1),
        "Clothing": (base * 0.7 + 10 * np.sin(np.arange(12) / 2) + rng.normal(0, 3, 12)).round(1),
        "Groceries": (np.full(12, 45) + rng.normal(0, 2, 12)).round(1),
    })


def get_students(n=200):
    """Student dataset for distributions and relationships.
    Columns: study_hours, sleep_hours, score, gender, grade_level"""
    rng = np.random.default_rng(SEED)
    study = rng.uniform(0, 10, n).round(1)
    sleep = rng.normal(7, 1.2, n).clip(4, 10).round(1)
    score = (35 + 5 * study + 2 * (sleep - 7) + rng.normal(0, 7, n)).clip(0, 100).round(0)
    return pd.DataFrame({
        "study_hours": study,
        "sleep_hours": sleep,
        "score": score,
        "gender": rng.choice(["Male", "Female"], n),
        "grade_level": rng.choice(["Freshman", "Sophomore", "Junior", "Senior"], n),
    })


def get_market_share():
    """Market share (%) of smartphone brands: parts of a whole."""
    return {"Brand A": 32, "Brand B": 25, "Brand C": 18, "Brand D": 12, "Others": 13}


def get_daily_visits(days=180):
    """Daily website visits with a weekly cycle, growth trend, noise and a marketing spike.
    Columns: date, visits, signups"""
    rng = np.random.default_rng(SEED)
    dates = pd.date_range("2026-01-01", periods=days, freq="D")
    t = np.arange(days)
    weekly = 1 - 0.25 * (dates.dayofweek >= 5)                 # weekends are quieter
    visits = (2000 + 8 * t) * weekly + rng.normal(0, 150, days)
    visits[100:107] *= 1.8                                     # a 7-day campaign spike
    visits = visits.round().astype(int)
    signups = (visits * rng.uniform(0.02, 0.04, days)).round().astype(int)
    return pd.DataFrame({"date": dates, "visits": visits, "signups": signups})


def get_restaurant_bills(n=240):
    """Restaurant bills (like seaborn's 'tips' dataset, but generated offline).
    Columns: total_bill, tip, size, day, time, smoker"""
    rng = np.random.default_rng(SEED)
    day = rng.choice(["Thu", "Fri", "Sat", "Sun"], n, p=[0.25, 0.15, 0.32, 0.28])
    time = np.where(np.isin(day, ["Sat", "Sun"]) | (rng.random(n) < 0.4), "Dinner", "Lunch")
    size = rng.choice([1, 2, 3, 4, 5, 6], n, p=[0.05, 0.55, 0.15, 0.17, 0.05, 0.03])
    total = (6 + 7 * size + np.where(time == "Dinner", 4, 0) + rng.gamma(2, 3, n)).round(2)
    tip = (total * rng.normal(0.16, 0.04, n)).clip(1).round(2)
    return pd.DataFrame({"total_bill": total, "tip": tip, "size": size, "day": day, "time": time,
                         "smoker": rng.choice(["Yes", "No"], n, p=[0.35, 0.65])})


def get_regional_sales():
    """Quarterly sales (in lakh) for 4 regions x 3 products, in LONG format.
    Columns: quarter, region, product, sales, target"""
    rng = np.random.default_rng(SEED)
    rows = []
    for q_i, quarter in enumerate(["Q1", "Q2", "Q3", "Q4"]):
        for r_i, region in enumerate(["North", "South", "East", "West"]):
            for p_i, product in enumerate(["Laptops", "Phones", "Tablets"]):
                sales = round(50 + 10 * q_i + 15 * r_i - 12 * p_i + float(rng.normal(0, 6)), 1)
                rows.append({"quarter": quarter, "region": region, "product": product,
                             "sales": sales, "target": round(55 + 8 * q_i + 10 * r_i - 10 * p_i, 1)})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- saving
def output_dir():
    """The output/ folder next to the script being run (each lecture keeps its own charts)."""
    script = pathlib.Path(sys.argv[0]).resolve()
    folder = script.parent if script.suffix == ".py" else pathlib.Path.cwd()
    path = folder / "output"
    path.mkdir(exist_ok=True)
    return path


def save_and_show(fig, filename, show=True, dpi=120):
    """Save a figure into <lecture>/output/ and optionally display it.
    With a non-interactive backend (python run_all.py sets MPLBACKEND=Agg) show() does nothing."""
    path = output_dir() / filename
    if not fig.get_constrained_layout():
        fig.tight_layout()
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    print(f"[saved] {path.parent.parent.name}/output/{filename}")
    if show:
        plt.show()
    plt.close(fig)
    return path
