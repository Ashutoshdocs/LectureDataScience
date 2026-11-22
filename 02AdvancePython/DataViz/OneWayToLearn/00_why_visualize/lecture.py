"""Lecture 00: Why visualize? Table vs chart, Anscombe's quartet, outliers, and the chart chooser."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from common import apply_style, get_monthly_sales, save_and_show  # noqa: E402

apply_style()
df = get_monthly_sales()

# ---------------------------------------------------------------- 1. table vs chart
print("=== 1. Raw data: can you spot the trend quickly? ===")
print(df.to_string(index=False))

fig, ax = plt.subplots()
ax.plot(df["Month"], df["Electronics"], marker="o", label="Electronics")
ax.plot(df["Month"], df["Clothing"], marker="s", label="Clothing")
ax.plot(df["Month"], df["Groceries"], marker="^", label="Groceries")
ax.set_title("Monthly Sales: A Chart Tells the Story Faster")      # every good chart has a title,
ax.set_xlabel("Month")                                             # axis labels,
ax.set_ylabel("Sales (in thousands)")
ax.legend()                                                        # and a legend
save_and_show(fig, "00a_table_vs_chart.png")
print("  In the chart: Electronics rises steadily, Clothing waves up and down, Groceries stays flat near 45.")

# ---------------------------------------------------------------- 2. Anscombe's quartet
print("\n=== 2. Anscombe's quartet: same statistics, different stories ===")
x = [10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5]
quartet = {
    "I": (x, [8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68]),
    "II": (x, [9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74]),
    "III": (x, [7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73]),
    "IV": ([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], [6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89]),
}
print(f"  {'set':<4} {'mean x':>7} {'mean y':>7} {'var y':>6} {'corr':>6} {'fit line':>16}")
fig, axes = plt.subplots(2, 2, figsize=(10, 7), sharex=True, sharey=True)
for ax, (name, (xs, ys)) in zip(axes.flat, quartet.items()):
    xs, ys = np.array(xs), np.array(ys)
    slope, intercept = np.polyfit(xs, ys, 1)
    r = np.corrcoef(xs, ys)[0, 1]
    print(f"  {name:<4} {xs.mean():7.2f} {ys.mean():7.2f} {ys.var(ddof=1):6.2f} {r:6.3f}   y = {slope:.2f}x + {intercept:.2f}")
    ax.scatter(xs, ys, color="tab:blue", edgecolor="k", zorder=3)
    line_x = np.array([3, 20])
    ax.plot(line_x, slope * line_x + intercept, color="tab:red", lw=1.5)
    ax.set_title(f"Dataset {name}: r = {r:.2f}")
fig.suptitle("Anscombe's Quartet: identical statistics, very different data", fontsize=15, fontweight="bold")
save_and_show(fig, "00b_anscombe.png")
print("  Same numbers in the table above, but: I is linear, II is curved, III has one outlier, IV is one extreme point.")

# ---------------------------------------------------------------- 3. outliers jump out
print("\n=== 3. A data error hides in a table but jumps out of a chart ===")
rng = np.random.default_rng(1)
temps = pd.Series(rng.normal(24, 1.5, 60).round(1))
temps[37] = 240.0                                   # a typo: 24.0 entered as 240
print("  describe():", temps.describe()[["mean", "min", "max"]].round(1).to_dict(), "<- easy to miss")
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(temps, marker=".", color="tab:gray")
ax.annotate("data-entry error?\n(24.0 typed as 240)", xy=(37, 240), xytext=(45, 180),
            arrowprops=dict(arrowstyle="->", color="red"), color="red")
ax.set_title("Hourly temperature readings")
ax.set_xlabel("Reading #")
ax.set_ylabel("Temperature (°C)")
save_and_show(fig, "00c_outlier.png")

# ---------------------------------------------------------------- 4. chart chooser
print("\n=== 4. Choosing a chart (preview of the course) ===")
fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes[0, 0].plot(df["Month"], df["Electronics"], marker="o")
axes[0, 0].set_title("Trend over time -> LINE")
axes[0, 1].bar(df["Month"][:6], df["Clothing"][:6], color="tab:orange")
axes[0, 1].set_title("Compare categories -> BAR")
axes[0, 2].pie([32, 25, 18, 25], labels=["A", "B", "C", "Other"], autopct="%1.0f%%")
axes[0, 2].set_title("Parts of a whole -> PIE")
axes[1, 0].stackplot(range(12), df["Electronics"], df["Clothing"], df["Groceries"], alpha=0.85)
axes[1, 0].set_title("Composition over time -> STACK")
values = rng.normal(65, 12, 300)
axes[1, 1].hist(values, bins=20, color="slateblue", edgecolor="white")
axes[1, 1].set_title("Distribution -> HISTOGRAM")
hx = rng.uniform(0, 10, 80)
axes[1, 2].scatter(hx, 35 + 5 * hx + rng.normal(0, 6, 80), alpha=0.7, edgecolor="k")
axes[1, 2].set_title("Relationship -> SCATTER")
for ax in axes.flat:
    ax.tick_params(labelsize=8)
axes[0, 0].tick_params(axis="x", rotation=45)
fig.suptitle("Pick the chart from the question you are asking", fontsize=16, fontweight="bold")
save_and_show(fig, "00d_chart_chooser.png")
