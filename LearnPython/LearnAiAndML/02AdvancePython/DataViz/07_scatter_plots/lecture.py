"""Lecture 07: Scatter plots: trend line + r, colour/size encodings, groups, correlation gallery, labels, overplotting."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import apply_style, get_students, save_and_show  # noqa: E402

apply_style()
df = get_students()

# ---------------------------------------------------------------- 1. trend + encodings (your original demo)
print("=== 1. Trend line + correlation; colour = sleep, size = score ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
ax1.scatter(df["study_hours"], df["score"], alpha=0.6, edgecolor="k")
slope, intercept = np.polyfit(df["study_hours"], df["score"], 1)
xs = np.linspace(0, 10, 50)
ax1.plot(xs, slope * xs + intercept, color="red", label=f"Trend: y = {slope:.1f}x + {intercept:.1f}")
corr = df["study_hours"].corr(df["score"])
ax1.set_title(f"Study Hours vs Score (r = {corr:.2f})")
ax1.set_xlabel("Study hours per day")
ax1.set_ylabel("Score")
ax1.legend()
sc = ax2.scatter(df["study_hours"], df["score"], c=df["sleep_hours"], cmap="viridis", s=df["score"] * 1.5,
                 alpha=0.7, edgecolor="k")
fig.colorbar(sc, ax=ax2, label="Sleep hours")
ax2.set_title("Color = Sleep Hours, Size = Score")
ax2.set_xlabel("Study hours per day")
ax2.set_ylabel("Score")
print(f"  each extra study hour adds about {slope:.1f} points; r = {corr:.2f} (strong positive)")
save_and_show(fig, "07a_scatter_trend_encodings.png")

# ---------------------------------------------------------------- 2. categorical colours + labels
print("\n=== 2. One scatter per group; label the top 3 ===")
fig, ax = plt.subplots()
markers = {"Freshman": "o", "Sophomore": "s", "Junior": "^", "Senior": "D"}
for level, marker in markers.items():
    sub = df[df["grade_level"] == level]
    ax.scatter(sub["study_hours"], sub["score"], marker=marker, alpha=0.75, label=f"{level} (n={len(sub)})")
for _, row in df.nlargest(3, "score").iterrows():
    ax.annotate(f"{row['score']:.0f}", (row["study_hours"], row["score"]), xytext=(-18, 6),
                textcoords="offset points", fontweight="bold")
ax.set_title("Score vs study hours by grade level (top 3 labelled)")
ax.set_xlabel("Study hours per day")
ax.set_ylabel("Score")
ax.legend(title="Grade", loc="lower right")
save_and_show(fig, "07b_scatter_groups_labels.png")

# ---------------------------------------------------------------- 3. correlation gallery
print("\n=== 3. What different r values look like ===")
rng = np.random.default_rng(1)
fig, axes = plt.subplots(2, 4, figsize=(15, 7))
x = rng.normal(0, 1, 300)
for ax, target in zip(axes[0], [0.95, 0.7, 0.3, 0.0]):
    y = target * x + np.sqrt(1 - target ** 2) * rng.normal(0, 1, 300)
    ax.scatter(x, y, s=10, alpha=0.6)
    ax.set_title(f"r = {np.corrcoef(x, y)[0, 1]:.2f}")
for ax, target in zip(axes[1][:2], [-0.7, -0.95]):
    y = target * x + np.sqrt(1 - target ** 2) * rng.normal(0, 1, 300)
    ax.scatter(x, y, s=10, alpha=0.6, color="tab:red")
    ax.set_title(f"r = {np.corrcoef(x, y)[0, 1]:.2f}")
curve_y = x ** 2 + rng.normal(0, 0.3, 300)
axes[1][2].scatter(x, curve_y, s=10, alpha=0.6, color="tab:green")
axes[1][2].set_title(f"curve: r = {np.corrcoef(x, curve_y)[0, 1]:.2f} (!)")
outlier_x = np.r_[rng.normal(0, 1, 30), 8]
outlier_y = np.r_[rng.normal(0, 1, 30), 8]
axes[1][3].scatter(outlier_x, outlier_y, s=14, color="tab:purple")
axes[1][3].set_title(f"one outlier: r = {np.corrcoef(outlier_x, outlier_y)[0, 1]:.2f} (!)")
for ax in axes.flat:
    ax.set_xticks([])
    ax.set_yticks([])
fig.suptitle("Correlation r measures LINEAR association only: always look at the plot", fontsize=15, fontweight="bold")
print(f"  a perfect U-shape has r = {np.corrcoef(x, curve_y)[0, 1]:.2f}; one outlier creates r = {np.corrcoef(outlier_x, outlier_y)[0, 1]:.2f}")
save_and_show(fig, "07c_correlation_gallery.png")

# ---------------------------------------------------------------- 4. linear vs quadratic fit
print("\n=== 4. Straight vs curved trend line ===")
hours = rng.uniform(0, 12, 150)
perf = 20 + 14 * hours - 0.9 * hours ** 2 + rng.normal(0, 6, 150)      # too much practice -> fatigue
fig, ax = plt.subplots()
ax.scatter(hours, perf, alpha=0.6, edgecolor="k")
grid = np.linspace(0, 12, 100)
for degree, color in [(1, "red"), (2, "green")]:
    coefs = np.polyfit(hours, perf, degree)
    ax.plot(grid, np.polyval(coefs, grid), color=color, lw=2.5, label=f"degree {degree} fit")
ax.set_title("Practice hours vs performance: a curve fits better")
ax.set_xlabel("Practice hours per day")
ax.set_ylabel("Performance")
ax.legend()
save_and_show(fig, "07d_linear_vs_quadratic.png")

# ---------------------------------------------------------------- 5. overplotting
print("\n=== 5. Overplotting: 50,000 points ===")
bx = rng.normal(0, 1, 50_000)
by = 0.5 * bx + rng.normal(0, 1, 50_000)
fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), sharex=True, sharey=True)
axes[0].scatter(bx, by, s=8)
axes[0].set_title("plain scatter: a solid blob")
axes[1].scatter(bx, by, s=4, alpha=0.03, color="black")
axes[1].set_title("alpha=0.03, s=4: density appears")
hb = axes[2].hexbin(bx, by, gridsize=35, cmap="viridis", mincnt=1)
fig.colorbar(hb, ax=axes[2], label="points per hexagon")
axes[2].set_title("hexbin: counts per cell")
save_and_show(fig, "07e_overplotting.png")
