"""
03 - Bar Charts in Matplotlib
-----------------------------
Covers: vertical bars, grouped (side-by-side) bars, horizontal bars,
and adding value labels on top of bars.
"""

import numpy as np
import matplotlib.pyplot as plt
from common import apply_style, get_monthly_sales, save_and_show

apply_style()
df = get_monthly_sales().head(6)  # first 6 months keeps it readable

# --- 1. Simple vertical bar chart ---
fig, ax = plt.subplots()
bars = ax.bar(df["Month"], df["Electronics"], color="steelblue")
ax.bar_label(bars, fmt="%.0f")  # value label on each bar
ax.set_title("Electronics Sales (Jan-Jun)")
ax.set_ylabel("Sales (in thousands)")
save_and_show(fig, "03a_bar_simple.png")

# --- 2. Grouped bar chart: shift each group by a bar width ---
x = np.arange(len(df))   # positions 0..5
width = 0.27
fig, ax = plt.subplots()
ax.bar(x - width, df["Electronics"], width, label="Electronics")
ax.bar(x,         df["Clothing"],    width, label="Clothing")
ax.bar(x + width, df["Groceries"],   width, label="Groceries")
ax.set_xticks(x, df["Month"])
ax.set_title("Grouped Bar Chart: Sales by Category")
ax.set_ylabel("Sales (in thousands)")
ax.legend()
save_and_show(fig, "03b_bar_grouped.png")

# --- 3. Horizontal bar chart (good for long category names) ---
totals = df[["Electronics", "Clothing", "Groceries"]].sum().sort_values()
fig, ax = plt.subplots()
hbars = ax.barh(totals.index, totals.values, color=["#8fbc8f", "#f4a460", "#6495ed"])
ax.bar_label(hbars, fmt="%.0f", padding=3)
ax.set_title("Total Sales Jan-Jun (Horizontal)")
ax.set_xlabel("Sales (in thousands)")
save_and_show(fig, "03c_bar_horizontal.png")
