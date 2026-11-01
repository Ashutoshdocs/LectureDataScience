import matplotlib.pyplot as plt
import numpy as np
from common import apply_style, get_monthly_sales, save_and_show

apply_style()
df = get_monthly_sales()
categories = ["Electronics", "Clothing", "Groceries"]
x = np.arange(len(df))  # Creates an array of numerical indices (0, 1, 2...) for the X-axis positions

# Generates 2 subplots stacked vertically (2 rows, 1 column) that share the same X-axis constraints
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

# --- 1. Absolute values: how big is each part and the total ---
# Plots categories on top of each other; the cumulative height represents total sales
ax1.stackplot(
    x,
    df["Electronics"],
    df["Clothing"],
    df["Groceries"],
    labels=categories,
    alpha=0.85,  # Sets opacity to 85% so background grid lines can subtly peek through
)
ax1.set_title("Stack Plot: Total Sales Built from Categories")
ax1.set_ylabel("Sales (in thousands)")
ax1.legend(loc="upper left")

# --- 2. 100% stack plot: how the share of each part changes ---
# Normalises each row: divides each category by the row total and multiplies by 100 to get percentages
share = df[categories].div(df[categories].sum(axis=1), axis=0) * 100

# Plots the percentage shares over time instead of raw currency/volume amounts
ax2.stackplot(
    x,
    share["Electronics"],
    share["Clothing"],
    share["Groceries"],
    labels=categories,
    alpha=0.85,
)
ax2.set_title("100% Stack Plot: Share of Each Category")
ax2.set_ylabel("Share (%)")
ax2.set_ylim(0, 100)  # Locks the vertical boundaries strictly between 0% and 100%
ax2.set_xticks(
    x, df["Month"]
)  # Maps the text labels (Jan, Feb...) onto the shared X positions (applies to both plots due to sharex=True)

save_and_show(fig, "05_stack_plots.png")
