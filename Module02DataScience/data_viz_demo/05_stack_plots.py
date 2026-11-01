"""
05 - Stack Plots in Matplotlib
------------------------------
A stack plot (stacked area chart) shows how several parts add up to a
total over time. The top edge = total; each band = one category.
"""

import numpy as np
import matplotlib.pyplot as plt
from common import apply_style, get_monthly_sales, save_and_show

apply_style()
df = get_monthly_sales()
categories = ["Electronics", "Clothing", "Groceries"]
x = np.arange(len(df))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True)

# --- 1. Absolute values: how big is each part and the total ---
ax1.stackplot(x, df["Electronics"], df["Clothing"], df["Groceries"],
              labels=categories, alpha=0.85)
ax1.set_title("Stack Plot: Total Sales Built from Categories")
ax1.set_ylabel("Sales (in thousands)")
ax1.legend(loc="upper left")

# --- 2. 100% stack plot: how the share of each part changes ---
share = df[categories].div(df[categories].sum(axis=1), axis=0) * 100
ax2.stackplot(x, share["Electronics"], share["Clothing"], share["Groceries"],
              labels=categories, alpha=0.85)
ax2.set_title("100% Stack Plot: Share of Each Category")
ax2.set_ylabel("Share (%)")
ax2.set_ylim(0, 100)
ax2.set_xticks(x, df["Month"])

save_and_show(fig, "05_stack_plots.png")
