"""Lecture 08: Subplots: grids, axes indexing, sharex/sharey, GridSpec, subplot_mosaic, small multiples, insets."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import (CATEGORIES, apply_style, get_market_share, get_monthly_sales, get_regional_sales,  # noqa: E402
                    get_students, save_and_show)

apply_style()
sales = get_monthly_sales()
students = get_students()
share = get_market_share()

# ---------------------------------------------------------------- 1. 2x2 grid (your original demo)
print("=== 1. 2x2 grid: axes[row, col] ===")
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
print("  axes is a", type(axes).__name__, "with shape", axes.shape)
axes[0, 0].plot(sales["Month"], sales["Electronics"], marker="o")
axes[0, 0].set_title("Line: Electronics")
axes[0, 1].bar(sales["Month"], sales["Clothing"], color="orange")
axes[0, 1].set_title("Bar: Clothing")
for ax in (axes[0, 0], axes[0, 1]):
    ax.tick_params(axis="x", rotation=45)
axes[1, 0].hist(students["score"], bins=15, edgecolor="white")
axes[1, 0].set_title("Histogram: Scores")
axes[1, 1].scatter(students["study_hours"], students["score"], s=12)
axes[1, 1].set_title("Scatter: Study vs Score")
fig.suptitle("2x2 Subplot Dashboard", fontsize=16, fontweight="bold")
save_and_show(fig, "08a_subplots_grid.png")

# ---------------------------------------------------------------- 2. GridSpec (your original demo)
print("\n=== 2. GridSpec: one wide chart on top, two below ===")
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 2)
top = fig.add_subplot(gs[0, :])
left = fig.add_subplot(gs[1, 0])
right = fig.add_subplot(gs[1, 1])
top.stackplot(range(12), sales["Electronics"], sales["Clothing"], sales["Groceries"], labels=CATEGORIES)
top.set_xticks(range(12), sales["Month"])
top.set_title("Stack Plot (spans full width)")
top.legend(loc="upper left")
left.pie(share.values(), labels=share.keys(), autopct="%1.0f%%")
left.set_title("Market Share")
right.barh(list(share.keys()), list(share.values()), color="teal")
right.set_title("Market Share (bars)")
fig.suptitle("Custom Layout with GridSpec", fontsize=16, fontweight="bold")
save_and_show(fig, "08b_subplots_gridspec.png")

# ---------------------------------------------------------------- 3. subplot_mosaic
print("\n=== 3. subplot_mosaic: layouts by name ===")
fig, ax = plt.subplot_mosaic([["trend", "trend", "share"],
                              ["hist", "scatter", "share"]], figsize=(15, 8), layout="constrained")
print("  axes keys:", list(ax.keys()))
for cat in CATEGORIES:
    ax["trend"].plot(sales["Month"], sales[cat], marker="o", label=cat)
ax["trend"].legend(ncols=3)
ax["trend"].set_title("Monthly sales")
ax["share"].pie(share.values(), labels=share.keys(), autopct="%1.0f%%", wedgeprops={"width": 0.4})
ax["share"].set_title("Market share")
ax["hist"].hist(students["score"], bins=15, color="slateblue", edgecolor="white")
ax["hist"].set_title("Score distribution")
ax["scatter"].scatter(students["study_hours"], students["score"], s=12, alpha=0.6)
ax["scatter"].set_title("Study vs score")
fig.suptitle("subplot_mosaic dashboard", fontsize=16, fontweight="bold")
save_and_show(fig, "08c_subplot_mosaic.png")

# ---------------------------------------------------------------- 4. sharex / sharey
print("\n=== 4. sharey matters for fair comparisons ===")
for share_y in (False, True):
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.8), sharey=share_y)
    for ax, cat in zip(axes, CATEGORIES):
        ax.plot(range(12), sales[cat], marker="o")
        ax.set_title(cat)
        ax.set_xticks(range(0, 12, 3), sales["Month"][::3])
    fig.suptitle(f"sharey={share_y}: " + ("every chart looks equally dramatic" if not share_y
                 else "true sizes are comparable: Electronics grew most"), fontsize=13, fontweight="bold")
    save_and_show(fig, f"08d_sharey_{share_y}.png")

# ---------------------------------------------------------------- 5. small multiples vs spaghetti
print("\n=== 5. Small multiples vs one crowded chart ===")
reg = get_regional_sales()
series = reg.groupby(["region", "product", "quarter"])["sales"].sum().unstack("quarter")
fig, ax = plt.subplots(figsize=(9, 5))
for (region, product), row in series.iterrows():
    ax.plot(row.index, row.values, marker="o", label=f"{region}-{product}")
ax.legend(ncols=3, fontsize=7)
ax.set_title("12 lines on one chart: spaghetti")
save_and_show(fig, "08e_spaghetti.png")

regions = ["North", "South", "East", "West"]
fig, axes = plt.subplots(1, 4, figsize=(16, 4), sharey=True, layout="constrained")
for ax, region in zip(axes, regions):
    for product in ["Laptops", "Phones", "Tablets"]:
        ax.plot(series.columns, series.loc[(region, product)], marker="o", label=product)
    ax.set_title(region)
axes[0].legend()
fig.supylabel("Sales (lakh)")
fig.suptitle("Small multiples: one panel per region, shared y-axis", fontsize=14, fontweight="bold")
save_and_show(fig, "08f_small_multiples.png")

# ---------------------------------------------------------------- 6. unequal sizes, empty cells, inset
print("\n=== 6. width_ratios, removing an unused cell, and an inset zoom ===")
fig, axes = plt.subplots(2, 3, figsize=(14, 7), gridspec_kw={"width_ratios": [2, 1, 1]})
axes[0, 0].plot(sales["Month"], sales["Electronics"], marker="o")
axes[0, 0].set_title("wide (width_ratio 2)")
inset = axes[0, 0].inset_axes([0.05, 0.55, 0.35, 0.4])
inset.plot(range(3), sales["Electronics"][:3], marker="o", color="tab:red")
inset.set_xticks(range(3), sales["Month"][:3], fontsize=7)
inset.set_title("Q1 zoom", fontsize=8)
axes[0, 0].indicate_inset_zoom(inset, edgecolor="gray")
for i, ax in enumerate([axes[0, 1], axes[0, 2], axes[1, 0], axes[1, 1]]):
    ax.bar(["a", "b", "c"], np.random.default_rng(i).integers(2, 10, 3), color=f"C{i + 1}")
    ax.set_title(f"panel {i + 2}")
axes[1, 2].remove()                                     # unused cell
fig.suptitle("Unequal widths, an inset, and a removed empty cell", fontsize=14, fontweight="bold")
save_and_show(fig, "08g_ratios_inset.png")
