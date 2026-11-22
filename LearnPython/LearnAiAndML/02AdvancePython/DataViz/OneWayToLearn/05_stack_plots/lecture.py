"""Lecture 05: Stack plots: absolute vs 100%, the wavy-baseline problem, band order, total line, streamgraph."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import CATEGORIES, apply_style, get_monthly_sales, save_and_show  # noqa: E402

apply_style()
df = get_monthly_sales()
x = np.arange(len(df))

# ---------------------------------------------------------------- 1. absolute and 100% (your original demo)
print("=== 1. Absolute stack and 100% stack ===")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)
ax1.stackplot(x, df["Electronics"], df["Clothing"], df["Groceries"], labels=CATEGORIES, alpha=0.85)
total = df[CATEGORIES].sum(axis=1)
ax1.plot(x, total, color="black", ls="--", lw=1.5, label="Total")
ax1.set_title("Stack Plot: Total Sales Built from Categories")
ax1.set_ylabel("Sales (in thousands)")
ax1.legend(loc="upper left", ncols=4)
ax1.set_ylim(0, total.max() * 1.15)

share = df[CATEGORIES].div(df[CATEGORIES].sum(axis=1), axis=0) * 100
ax2.stackplot(x, share.T, labels=CATEGORIES, alpha=0.85)       # a 2-D array works too
ax2.set_title("100% Stack Plot: Share of Each Category")
ax2.set_ylabel("Share (%)")
ax2.set_ylim(0, 100)
ax2.set_xticks(x, df["Month"])
for cat, ypos in zip(CATEGORIES, [15, 50, 85]):
    ax2.text(0.2, ypos, cat, color="white", fontweight="bold", va="center")
print(f"  total grew from {total.iloc[0]:.0f} to {total.iloc[-1]:.0f}")
print(f"  Groceries share fell from {share['Groceries'].iloc[0]:.0f}% to {share['Groceries'].iloc[-1]:.0f}%")
save_and_show(fig, "05a_stack_absolute_and_100.png")

# ---------------------------------------------------------------- 2. the wavy-baseline problem
print("\n=== 2. Upper bands are hard to read: Groceries is flat, but in a stack it looks wavy ===")
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), sharey=False)
axes[0].stackplot(x, df["Electronics"], df["Clothing"], df["Groceries"], labels=CATEGORIES, alpha=0.85)
axes[0].set_title("Groceries on top: looks wavy")
axes[1].stackplot(x, df["Groceries"], df["Electronics"], df["Clothing"],
                  labels=["Groceries", "Electronics", "Clothing"], colors=["tab:green", "tab:blue", "tab:orange"], alpha=0.85)
axes[1].set_title("Groceries at the bottom: flat")
for cat in CATEGORIES:
    axes[2].plot(x, df[cat], marker="o", label=cat)
axes[2].set_title("Separate lines: every trend readable")
axes[2].set_ylim(0, 80)
for ax in axes:
    ax.set_xticks(x[::2], df["Month"][::2])
    ax.legend(loc="upper left", fontsize=8)
print(f"  Groceries really ranges only {df['Groceries'].min()}-{df['Groceries'].max()}")
save_and_show(fig, "05b_stack_baseline_problem.png")

# ---------------------------------------------------------------- 3. streamgraph
print("\n=== 3. Streamgraph: baseline='wiggle' ===")
rng = np.random.default_rng(3)
weeks = np.arange(52)
genres = ["Pop", "Rock", "Hip-hop", "Jazz", "Classical"]
streams = [np.clip(50 + 30 * np.sin((weeks + i * 9) / 8) + rng.normal(0, 4, 52), 5, None) for i in range(5)]
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.stackplot(weeks, streams, labels=genres, baseline="wiggle", alpha=0.9)
ax.set_title("Weekly streams by genre (streamgraph)")
ax.set_xlabel("Week of year")
ax.set_yticks([])                                       # absolute y has no meaning with a wiggle baseline
ax.legend(loc="upper left", ncols=5, fontsize=9)
save_and_show(fig, "05c_streamgraph.png")
