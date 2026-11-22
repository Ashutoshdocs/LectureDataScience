"""Lecture 16: Ten classic visualization mistakes, each drawn as BAD (left) vs FIXED (right)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from common import CATEGORIES, apply_style, get_monthly_sales, get_regional_sales, save_and_show  # noqa: E402

apply_style()
rng = np.random.default_rng(7)
sales = get_monthly_sales()


def pair(title_bad, title_good, figsize=(14, 4.8), **kw):
    fig, (bad, good) = plt.subplots(1, 2, figsize=figsize, **kw)
    bad.set_title("BAD: " + title_bad, color="firebrick")
    good.set_title("FIXED: " + title_good, color="darkgreen")
    return fig, bad, good


# 1 ---------------------------------------------------------------- truncated axis
print("=== 1. Truncated y-axis on bars ===")
vals = {"Plan A": 96.5, "Plan B": 98.0, "Plan C": 99.2}
fig, bad, good = pair("axis starts at 96", "bars start at 0")
bad.bar(vals.keys(), vals.values(), color="tab:red")
bad.set_ylim(96, 99.5)
good.bar(vals.keys(), vals.values(), color="tab:blue")
good.bar_label(good.containers[0], fmt="%.1f%%")
good.set_ylim(0, 110)
print(f"  C is {vals['Plan C'] / vals['Plan A'] - 1:.1%} higher than A, but the truncated bars make it look ~4x taller")
save_and_show(fig, "16_01_truncated_axis.png")

# 2 ---------------------------------------------------------------- pie with many slices
print("\n=== 2. Pie with many slices ===")
cats = pd.Series(rng.integers(5, 30, 9), index=[f"Product {c}" for c in "ABCDEFGHI"]).sort_values()
fig, bad, good = pair("9-slice pie", "sorted horizontal bars", figsize=(14, 5.5))
bad.pie(cats, labels=cats.index, textprops={"fontsize": 8})
hb = good.barh(cats.index, cats.values, color=["tab:blue" if v == cats.max() else "0.7" for v in cats])
good.bar_label(hb, padding=3)
save_and_show(fig, "16_02_pie_many_slices.png")

# 3 ---------------------------------------------------------------- spaghetti
print("\n=== 3. Spaghetti lines ===")
series = pd.DataFrame(np.cumsum(rng.normal(0.5, 2, (12, 9)), axis=0) + 50, columns=[f"Store {i}" for i in range(1, 10)])
focus = series.iloc[-1].idxmax()
fig, bad, good = pair("9 tangled colours", f"highlight {focus}, grey the rest")
series.plot(ax=bad, legend=True)
bad.legend(fontsize=7, ncols=3)
for col in series:
    good.plot(series.index, series[col], color="tab:blue" if col == focus else "0.8", lw=3 if col == focus else 1)
good.text(11.2, series[focus].iloc[-1], focus, color="tab:blue", va="center", fontweight="bold")
good.set_xlim(0, 13.5)
save_and_show(fig, "16_03_spaghetti.png")

# 4 ---------------------------------------------------------------- dual axes
print("\n=== 4. Dual axes with arbitrary scales ===")
months = np.arange(12)
ice_cream = 100 + 8 * months + rng.normal(0, 5, 12)
umbrellas = 300 - 2 * months + rng.normal(0, 3, 12)
fig, bad, good = pair("two y-axes make unrelated series 'track'", "index both to 100 (or use two panels)")
bad.plot(months, ice_cream, color="tab:orange")
twin = bad.twinx()
twin.plot(months, umbrellas, color="tab:purple")
twin.set_ylim(umbrellas.max() + 2, umbrellas.min() - 30)        # an inverted, cherry-picked scale
twin.grid(False)
good.plot(months, ice_cream / ice_cream[0] * 100, color="tab:orange", label="ice cream")
good.plot(months, umbrellas / umbrellas[0] * 100, color="tab:purple", label="umbrellas")
good.axhline(100, color="gray", lw=0.8)
good.set_ylabel("Index (January = 100)")
good.legend()
print(f"  real correlation: {np.corrcoef(ice_cream, umbrellas)[0, 1]:.2f} (they move in OPPOSITE directions)")
save_and_show(fig, "16_04_dual_axes.png")

# 5 ---------------------------------------------------------------- rainbow colormap
print("\n=== 5. Rainbow colormap ===")
grid = np.add.outer(np.linspace(0, 1, 60), np.linspace(0, 1, 60))
fig, bad, good = pair("'jet' invents bands", "'viridis' is smooth & colour-blind safe", figsize=(12, 5))
bad.imshow(grid, cmap="jet")
good.imshow(grid, cmap="viridis")
for ax in (bad, good):
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
save_and_show(fig, "16_05_rainbow_colormap.png")

# 6 ---------------------------------------------------------------- 3-D effects
print("\n=== 6. 3-D bars ===")
fig = plt.figure(figsize=(14, 4.8))
bad = fig.add_subplot(1, 2, 1, projection="3d")
q = [42, 55, 48, 61]
bad.bar3d(np.arange(4), np.zeros(4), np.zeros(4), 0.6, 0.6, q, color="tab:red", alpha=0.8)
bad.set_xticks(np.arange(4) + 0.3, ["Q1", "Q2", "Q3", "Q4"])
bad.set_title("BAD: 3-D perspective distorts heights", color="firebrick")
good = fig.add_subplot(1, 2, 2)
gb = good.bar(["Q1", "Q2", "Q3", "Q4"], q, color="tab:blue")
good.bar_label(gb)
good.set_title("FIXED: flat 2-D with labels", color="darkgreen")
save_and_show(fig, "16_06_3d_effects.png")

# 7 ---------------------------------------------------------------- unsorted
print("\n=== 7. Unsorted categories ===")
reg = get_regional_sales().groupby("region")["sales"].sum()
reg = pd.concat([reg, pd.Series({"Central": 610.0, "Islands": 240.0, "Metro": 1020.0})])
fig, bad, good = pair("alphabetical order", "sorted by value")
bad.bar(reg.index, reg.values, color="tab:gray")
s = reg.sort_values()
good.barh(s.index, s.values, color="tab:blue")
save_and_show(fig, "16_07_unsorted.png")

# 8 ---------------------------------------------------------------- overplotting
print("\n=== 8. Overplotting ===")
x = rng.normal(0, 1, 30_000)
y = x * 0.4 + rng.normal(0, 1, 30_000)
fig, bad, good = pair("30k opaque dots: one blob", "hexbin reveals the density")
bad.scatter(x, y, s=10)
hb = good.hexbin(x, y, gridsize=40, cmap="viridis", mincnt=1)
fig.colorbar(hb, ax=good)
save_and_show(fig, "16_08_overplotting.png")

# 9 ---------------------------------------------------------------- bars of means
print("\n=== 9. Bars of means hide the data ===")
demo = pd.DataFrame({"team": np.repeat(["Team X", "Team Y"], 60),
                     "hours": np.r_[rng.normal(40, 2, 60), np.r_[rng.normal(30, 2, 30), rng.normal(50, 2, 30)]]})
fig, bad, good = pair("identical bars", "the strip plot shows Team Y is split in two")
sns.barplot(data=demo, x="team", y="hours", ax=bad, errorbar=None, color="tab:gray")
sns.boxplot(data=demo, x="team", y="hours", ax=good, color="0.9", fliersize=0)
sns.stripplot(data=demo, x="team", y="hours", ax=good, color="tab:blue", size=4)
save_and_show(fig, "16_09_bars_hide_data.png")

# 10 --------------------------------------------------------------- missing context
print("\n=== 10. Missing context ===")
fig, bad, good = pair("no title, labels, units or message", "insight title, units, annotation, source")
bad.plot(sales["Electronics"])
bad.set_title("")
good.plot(sales["Month"], sales["Electronics"], marker="o", color="tab:blue")
good.set_title("Electronics sales grew 78% in 2026", loc="left", fontweight="bold")
good.set_ylabel("Sales (Rs thousands)")
good.annotate("record month", xy=(11, sales["Electronics"].iloc[-1]), xytext=(7, 72), arrowprops=dict(arrowstyle="->"))
good.text(0, -0.15, "Source: internal sales system, Jan-Dec 2026", transform=good.transAxes, fontsize=8, color="gray")
good.tick_params(axis="x", labelsize=8)
save_and_show(fig, "16_10_missing_context.png")

# ---------------------------------------------------------------- chart chooser summary figure
print("\n=== Bonus: one dataset, five questions, five charts ===")
long = sales.melt(id_vars="Month", var_name="Category", value_name="Sales")
fig, axes = plt.subplots(1, 5, figsize=(22, 4.2))
sns.barplot(data=long, x="Sales", y="Category", estimator="sum", errorbar=None, order=CATEGORIES, ax=axes[0])
axes[0].set_title("Which category sells most?\n-> sorted bar")
sns.lineplot(data=long, x="Month", y="Sales", hue="Category", ax=axes[1])
axes[1].set_title("How do sales change?\n-> line")
axes[1].tick_params(axis="x", rotation=90)
totals = sales[CATEGORIES].sum()
axes[2].pie(totals, labels=totals.index, autopct="%1.0f%%")
axes[2].set_title("What share does each have?\n-> pie (3 parts)")
sns.boxplot(data=long, x="Category", y="Sales", ax=axes[3])
axes[3].set_title("How variable is each?\n-> box")
sns.scatterplot(data=sales, x="Electronics", y="Clothing", ax=axes[4])
axes[4].set_title("Do they move together?\n-> scatter")
save_and_show(fig, "16_11_question_to_chart.png")
