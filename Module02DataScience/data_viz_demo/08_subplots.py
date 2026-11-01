"""
08 - Subplots in Matplotlib
---------------------------
Subplots put several charts in one figure. Covers: plt.subplots grid,
indexing axes, sharex/sharey, a figure-level title, and GridSpec for
uneven layouts. Builds a mini "dashboard" from the shared data.
"""

import matplotlib.pyplot as plt
from common import (apply_style, get_monthly_sales, get_students,
                    get_market_share, save_and_show)

apply_style()
sales = get_monthly_sales()
students = get_students()
share = get_market_share()

# --- 1. Regular 2x2 grid: axes is a 2D array -> axes[row, col] ---
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(sales["Month"], sales["Electronics"], marker="o")
axes[0, 0].set_title("Line: Electronics")

axes[0, 1].bar(sales["Month"], sales["Clothing"], color="orange")
axes[0, 1].set_title("Bar: Clothing")
axes[0, 1].tick_params(axis="x", rotation=45)

axes[1, 0].hist(students["score"], bins=15, edgecolor="white")
axes[1, 0].set_title("Histogram: Scores")

axes[1, 1].scatter(students["study_hours"], students["score"], s=12)
axes[1, 1].set_title("Scatter: Study vs Score")

fig.suptitle("2x2 Subplot Dashboard", fontsize=16, fontweight="bold")
save_and_show(fig, "08a_subplots_grid.png")

# --- 2. GridSpec: one wide chart on top, two below ---
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 2)
top = fig.add_subplot(gs[0, :])      # spans both columns
left = fig.add_subplot(gs[1, 0])
right = fig.add_subplot(gs[1, 1])

top.stackplot(range(12), sales["Electronics"], sales["Clothing"], sales["Groceries"],
              labels=["Electronics", "Clothing", "Groceries"])
top.set_xticks(range(12), sales["Month"])
top.set_title("Stack Plot (spans full width)")
top.legend(loc="upper left")

left.pie(share.values(), labels=share.keys(), autopct="%1.0f%%")
left.set_title("Market Share")

right.barh(list(share.keys()), list(share.values()), color="teal")
right.set_title("Market Share (bars)")

fig.suptitle("Custom Layout with GridSpec", fontsize=16, fontweight="bold")
save_and_show(fig, "08b_subplots_gridspec.png")
