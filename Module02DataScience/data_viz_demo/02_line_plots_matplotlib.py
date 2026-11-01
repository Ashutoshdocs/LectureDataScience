"""
02 - Plotting Charts using Matplotlib (Line Plots)
--------------------------------------------------
Covers: plt.plot, colors, line styles, markers, labels, legend,
grid, annotations, and the two Matplotlib interfaces (pyplot vs OO).
"""

import numpy as np
import matplotlib.pyplot as plt
from common import apply_style, get_monthly_sales, save_and_show

apply_style()
df = get_monthly_sales()

# --- Style 1: pyplot (quick, MATLAB-like) ---
plt.figure()
x = np.linspace(0, 10, 100)
plt.plot(x, np.sin(x), label="sin(x)")
plt.plot(x, np.cos(x), label="cos(x)", linestyle="--")
plt.title("pyplot interface: sin and cos")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
save_and_show(plt.gcf(), "02a_pyplot_basic.png")

# --- Style 2: Object-Oriented (recommended for real projects) ---
fig, ax = plt.subplots()

# Format customization: color, linestyle, marker, linewidth
ax.plot(df["Month"], df["Electronics"], color="#1f77b4", linestyle="-",
        marker="o", linewidth=2, label="Electronics")
ax.plot(df["Month"], df["Clothing"], color="#ff7f0e", linestyle="--",
        marker="s", linewidth=2, label="Clothing")
ax.plot(df["Month"], df["Groceries"], color="#2ca02c", linestyle=":",
        marker="^", linewidth=2, label="Groceries")

# Annotate the highest point
best = df["Electronics"].idxmax()
ax.annotate("Peak", xy=(best, df["Electronics"][best]),
            xytext=(best - 2, df["Electronics"][best] + 5),
            arrowprops=dict(arrowstyle="->"))

ax.set_title("Monthly Sales by Category (OO interface)")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (in thousands)")
ax.set_ylim(0, 90)
ax.legend(loc="lower right")

save_and_show(fig, "02b_line_chart.png")
