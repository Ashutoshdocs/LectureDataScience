"""Lecture 03: Bar charts: simple, grouped, horizontal ranking, stacked, 100% stacked, error bars, highlighting."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import CATEGORIES, apply_style, get_monthly_sales, get_students, save_and_show  # noqa: E402

apply_style()
full = get_monthly_sales()
df = full.head(6)                                     # Jan-Jun keeps the bars readable

# ---------------------------------------------------------------- 1. simple
print("=== 1. Simple vertical bars with value labels ===")
fig, ax = plt.subplots()
bars = ax.bar(df["Month"], df["Electronics"], color="steelblue")
ax.bar_label(bars, fmt="%.0f", padding=2)            # value on top of each bar
ax.set_title("Electronics Sales (Jan-Jun)")
ax.set_ylabel("Sales (in thousands)")
save_and_show(fig, "03a_bar_simple.png")

# ---------------------------------------------------------------- 2. grouped
print("\n=== 2. Grouped bars: shift each series by one width ===")
x = np.arange(len(df))
width = 0.27
fig, ax = plt.subplots()
for offset, cat in zip([-width, 0, width], CATEGORIES):
    ax.bar(x + offset, df[cat], width, label=cat)
ax.set_xticks(x, df["Month"])                         # readable labels at the group centres
ax.set_title("Grouped Bar Chart: Sales by Category")
ax.set_ylabel("Sales (in thousands)")
ax.legend(ncols=3, loc="upper left")
ax.set_ylim(0, 70)
print("  positions used:", {cat: (x + o).round(2).tolist()[:3] for o, cat in zip([-width, 0, width], CATEGORIES)}, "...")
save_and_show(fig, "03b_bar_grouped.png")

# ---------------------------------------------------------------- 3. horizontal ranking with highlight
print("\n=== 3. Horizontal, sorted ranking with one highlighted bar ===")
ranked = full.sort_values("Electronics")
colors = ["tab:orange" if v == ranked["Electronics"].max() else "lightgray" for v in ranked["Electronics"]]
fig, ax = plt.subplots(figsize=(8, 6))
hbars = ax.barh(ranked["Month"], ranked["Electronics"], color=colors)
ax.bar_label(hbars, fmt="%.1f", padding=3)
ax.set_title("Electronics: best month highlighted")
ax.set_xlabel("Sales (in thousands)")
ax.grid(False)
ax.spines[["top", "right"]].set_visible(False)
print("  best month:", ranked["Month"].iloc[-1])
save_and_show(fig, "03c_bar_horizontal_ranking.png")

# ---------------------------------------------------------------- 4. totals (your original horizontal chart)
totals = df[CATEGORIES].sum().sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
hb = ax.barh(totals.index, totals.values, color=["#8fbc8f", "#f4a460", "#6495ed"])
ax.bar_label(hb, fmt="%.0f", padding=3)
ax.set_title("Total Sales Jan-Jun by Category")
ax.set_xlabel("Sales (in thousands)")
ax.set_xlim(0, totals.max() * 1.15)
save_and_show(fig, "03d_bar_totals.png")

# ---------------------------------------------------------------- 5. stacked
print("\n=== 5. Stacked bars: bottom= ===")
fig, ax = plt.subplots()
bottom = np.zeros(len(df))
for cat in CATEGORIES:
    seg = ax.bar(df["Month"], df[cat], bottom=bottom, label=cat)
    ax.bar_label(seg, fmt="%.0f", label_type="center", color="white", fontsize=9)
    bottom += df[cat].to_numpy()
ax.bar_label(seg, labels=[f"{t:.0f}" for t in bottom], padding=3, fontweight="bold")   # totals on top
ax.set_title("Stacked Bar Chart: total and composition")
ax.set_ylabel("Sales (in thousands)")
ax.set_ylim(0, bottom.max() * 1.12)
ax.legend(loc="upper left", ncols=3)
save_and_show(fig, "03e_bar_stacked.png")

# ---------------------------------------------------------------- 6. 100% stacked horizontal
print("\n=== 6. 100% stacked horizontal bars by quarter ===")
q = full.assign(quarter=["Q1"] * 3 + ["Q2"] * 3 + ["Q3"] * 3 + ["Q4"] * 3).groupby("quarter")[CATEGORIES].sum()
share = q.div(q.sum(axis=1), axis=0) * 100
print(share.round(1).to_string())
fig, ax = plt.subplots(figsize=(9, 4))
left = np.zeros(len(share))
for cat in CATEGORIES:
    seg = ax.barh(share.index, share[cat], left=left, label=cat)
    ax.bar_label(seg, fmt="%.0f%%", label_type="center", color="white")
    left += share[cat].to_numpy()
ax.set_xlim(0, 100)
ax.invert_yaxis()                                     # Q1 at the top
ax.set_title("Share of sales by quarter (100% stacked)")
ax.set_xlabel("Share (%)")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), ncols=3)
save_and_show(fig, "03f_bar_100_stacked.png")

# ---------------------------------------------------------------- 7. error bars
print("\n=== 7. Mean score per grade with error bars (standard deviation) ===")
students = get_students()
order = ["Freshman", "Sophomore", "Junior", "Senior"]
stats = students.groupby("grade_level")["score"].agg(["mean", "std", "count"]).loc[order]
print(stats.round(1).to_string())
fig, ax = plt.subplots(figsize=(8, 5))
eb = ax.bar(stats.index, stats["mean"], yerr=stats["std"], capsize=6, color="mediumseagreen", edgecolor="black")
ax.bar_label(eb, fmt="%.1f", label_type="center", color="white", fontweight="bold")
ax.set_title("Mean exam score by grade (error bars = 1 std)")
ax.set_ylabel("Score")
ax.set_ylim(0, 100)
save_and_show(fig, "03g_bar_error_bars.png")
