import matplotlib.pyplot as plt
import numpy as np
from common import apply_style, get_monthly_sales, save_and_show

apply_style()
df = get_monthly_sales().head(6)  # .head(6) extracts only the first 6 rows (Jan to Jun) for cleaner visual spacing

# --- 1. Simple vertical bar chart ---
fig, ax = plt.subplots()
bars = ax.bar(
    df["Month"], df["Electronics"], color="steelblue"
)  # Generates vertical bars for Electronics
ax.bar_label(
    bars, fmt="%.0f"
)  # Iterates through bars and overlays the exact value as text (formatted as an integer)
ax.set_title("Electronics Sales (Jan-Jun)")
ax.set_ylabel("Sales (in thousands)")
save_and_show(fig, "03a_bar_simple.png")

# --- 2. Grouped bar chart: shift each group by a bar width ---
x = np.arange(len(df))  # Creates an array of base coordinate indexes: [0, 1, 2, 3, 4, 5]
width = 0.27  # Defines how wide each individual category bar should be

fig, ax = plt.subplots()
# Shift columns manually along the X-axis using arithmetic off the baseline 'x'
ax.bar(x - width, df["Electronics"], width, label="Electronics")  # Shifted left
ax.bar(x, df["Clothing"], width, label="Clothing")  # Placed directly on the baseline
ax.bar(
    x + width, df["Groceries"], width, label="Groceries"
)  # Shifted right

ax.set_xticks(
    x, df["Month"]
)  # Replaces the raw baseline numbers (0..5) with human-readable Month text strings
ax.set_title("Grouped Bar Chart: Sales by Category")
ax.set_ylabel("Sales (in thousands)")
ax.legend()
save_and_show(fig, "03b_bar_grouped.png")

# --- 3. Horizontal bar chart (good for long category names) ---
# Sums columns horizontally across rows, then sorts categories from lowest total to highest
totals = df[["Electronics", "Clothing", "Groceries"]].sum().sort_values()

fig, ax = plt.subplots()
# 'barh' maps category names to the Y-axis and numerical totals to the X-axis width
hbars = ax.barh(
    totals.index, totals.values, color=["#8fbc8f", "#f4a460", "#6495ed"]
)
ax.bar_label(
    hbars, fmt="%.0f", padding=3
)  # Adds labels to the right of horizontal bars with 3 points of padding
ax.set_title("Total Sales Jan-Jun (Horizontal)")
ax.set_xlabel("Sales (in thousands)")
save_and_show(fig, "03c_bar_horizontal.png")
