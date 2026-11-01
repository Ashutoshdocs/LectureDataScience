"""
07 - Scatter Plots in Matplotlib
--------------------------------
A scatter plot shows the relationship between two numeric variables.
Covers: basic scatter, color by a 3rd variable (colormap + colorbar),
size by a 4th variable, and a trend line.
"""

import numpy as np
import matplotlib.pyplot as plt
from common import apply_style, get_students, save_and_show

apply_style()
df = get_students()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# --- 1. Basic scatter + linear trend line ---
ax1.scatter(df["study_hours"], df["score"], alpha=0.6, edgecolor="k")
slope, intercept = np.polyfit(df["study_hours"], df["score"], 1)
xs = np.linspace(0, 10, 50)
ax1.plot(xs, slope * xs + intercept, color="red",
         label=f"Trend: y = {slope:.1f}x + {intercept:.1f}")
corr = df["study_hours"].corr(df["score"])
ax1.set_title(f"Study Hours vs Score (r = {corr:.2f})")
ax1.set_xlabel("Study hours per day")
ax1.set_ylabel("Score")
ax1.legend()

# --- 2. Encode extra variables: color = sleep, size = score ---
sc = ax2.scatter(df["study_hours"], df["score"],
                 c=df["sleep_hours"], cmap="viridis",
                 s=df["score"] * 1.5, alpha=0.7, edgecolor="k")
fig.colorbar(sc, ax=ax2, label="Sleep hours")
ax2.set_title("Color = Sleep Hours, Size = Score")
ax2.set_xlabel("Study hours per day")
ax2.set_ylabel("Score")

save_and_show(fig, "07_scatter_plots.png")
