import matplotlib.pyplot as plt
import numpy as np
from common import apply_style, get_students, save_and_show

apply_style()
df = get_students()  # Fetches student dataset (columns: study_hours, score, sleep_hours)

# Generates a canvas with 1 row and 2 side-by-side axes (ax1 and ax2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# --- 1. Basic scatter + linear trend line ---
# Plots study hours on X and exam scores on Y; 'edgecolor="k"' gives markers a sharp black outline ('k' = black)
ax1.scatter(df["study_hours"], df["score"], alpha=0.6, edgecolor="k")

# Performs a least-squares polynomial fit of degree 1 (linear regression) to calculate slope and intercept
slope, intercept = np.polyfit(df["study_hours"], df["score"], 1)
xs = np.linspace(0, 10, 50)  # Creates 50 clean X points to span the study hours domain
# Plots the calculated line of best fit using the standard linear equation formula: y = mx + c
ax1.plot(
    xs,
    slope * xs + intercept,
    color="red",
    label=f"Trend: y = {slope:.1f}x + {intercept:.1f}",
)

corr = (
    df["study_hours"].corr(df["score"])
)  # Computes the Pearson correlation coefficient (r)
ax1.set_title(f"Study Hours vs Score (r = {corr:.2f})")
ax1.set_xlabel("Study hours per day")
ax1.set_ylabel("Score")
ax1.legend()

# --- 2. Encode extra variables: color = sleep, size = score ---
# 'c' maps fill color to sleep hours using the 'viridis' color spectrum
# 's' calculates dynamic bubble sizes proportional to the student's actual exam score
sc = ax2.scatter(
    df["study_hours"],
    df["score"],
    c=df["sleep_hours"],
    cmap="viridis",
    s=df["score"] * 1.5,
    alpha=0.7,
    edgecolor="k",
)
# Attaches an interactive structural colorbar key to the right side of the specific ax2 plot area
fig.colorbar(sc, ax=ax2, label="Sleep hours")
ax2.set_title("Color = Sleep Hours, Size = Score")
ax2.set_xlabel("Study hours per day")
ax2.set_ylabel("Score")

save_and_show(fig, "07_scatter_plots.png")
