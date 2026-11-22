"""Lecture 06: Histograms: bins, mean/median, density, cumulative, step overlays, distribution shapes, hist2d."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import apply_style, get_students, save_and_show  # noqa: E402

apply_style()
df = get_students()

# ---------------------------------------------------------------- 1. basic + mean/median
print("=== 1. Basic histogram with mean and median lines ===")
fig, ax = plt.subplots()
counts, edges, patches = ax.hist(df["score"], bins=15, color="slateblue", edgecolor="white")
mean, median = df["score"].mean(), df["score"].median()
ax.axvline(mean, color="red", linestyle="--", label=f"Mean = {mean:.1f}")
ax.axvline(median, color="black", linestyle=":", label=f"Median = {median:.1f}")
ax.set_title("Distribution of Exam Scores")
ax.set_xlabel("Score")
ax.set_ylabel("Number of students")
ax.legend()
print("  hist() returned", len(counts), "counts, e.g.", counts[:5].astype(int).tolist(), "...")
print("  bin edges:", edges[:4].round(1).tolist(), "... width", round(edges[1] - edges[0], 2))
save_and_show(fig, "06a_histogram_basic.png")

# ---------------------------------------------------------------- 2. bin count
print("\n=== 2. Bins: too few hides detail, too many is noisy ===")
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, bins in zip(axes, [5, 15, 50]):
    ax.hist(df["score"], bins=bins, edgecolor="white")
    ax.set_title(f"bins = {bins}")
save_and_show(fig, "06b_histogram_bins.png")

rng = np.random.default_rng(0)
bimodal = np.r_[rng.normal(35, 5, 300), rng.normal(65, 5, 300)]
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(bimodal, bins=4, color="gray", edgecolor="white")
axes[0].set_title("bins = 4: looks like one hump")
axes[1].hist(bimodal, bins="auto", color="tab:purple", edgecolor="white")
axes[1].set_title("bins = 'auto': two groups appear")
print("  'auto' chose", len(np.histogram_bin_edges(bimodal, bins="auto")) - 1, "bins for the bimodal data")
save_and_show(fig, "06c_bins_hide_bimodal.png")

# ---------------------------------------------------------------- 3. density, cumulative, step
print("\n=== 3. density=True, cumulative=True, histtype='step' ===")
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
axes[0].hist(df["score"], bins=15, density=True, color="teal", edgecolor="white")
axes[0].set_title("density=True (area = 1)")
axes[0].set_ylabel("Density")
c, e, _ = axes[1].hist(df["score"], bins=range(0, 101, 5), cumulative=True, color="darkorange", edgecolor="white")
below_50 = int(c[list(e).index(50) - 1])
axes[1].axvline(50, color="black", ls="--")
axes[1].text(52, below_50, f"{below_50} students\nscored < 50", va="top")
axes[1].set_title("cumulative=True")
for level in ["Freshman", "Senior"]:
    axes[2].hist(df.loc[df["grade_level"] == level, "score"], bins=range(0, 101, 10), histtype="step", lw=2.5, label=level)
axes[2].set_title("histtype='step' to overlay groups")
axes[2].legend()
for ax in axes:
    ax.set_xlabel("Score")
print(f"  {below_50} of {len(df)} students scored below 50")
save_and_show(fig, "06d_density_cumulative_step.png")

# ---------------------------------------------------------------- 4. overlapping groups (your original demo)
print("\n=== 4. Overlapping histograms: same bins + alpha ===")
fig, ax = plt.subplots()
bins = range(0, 101, 5)
for gender, color in [("Male", "tab:blue"), ("Female", "tab:pink")]:
    ax.hist(df.loc[df["gender"] == gender, "score"], bins=bins, alpha=0.6, label=gender, color=color, edgecolor="white")
ax.set_title("Scores by Gender (Overlapping)")
ax.set_xlabel("Score")
ax.set_ylabel("Count")
ax.legend()
print("  group sizes:", df["gender"].value_counts().to_dict())
save_and_show(fig, "06e_histogram_compare.png")

# ---------------------------------------------------------------- 5. shapes gallery
print("\n=== 5. Distribution shapes ===")
shapes = {
    "Symmetric (normal)": rng.normal(50, 10, 3000),
    "Right-skewed (incomes)": rng.lognormal(10, 0.6, 3000) / 1000,
    "Left-skewed": 100 - rng.gamma(2, 8, 3000),
    "Bimodal": bimodal,
    "Uniform": rng.uniform(0, 10, 3000),
    "With outliers": np.r_[rng.normal(50, 5, 2950), rng.uniform(95, 110, 50)],
}
fig, axes = plt.subplots(2, 3, figsize=(14, 7))
for ax, (name, values) in zip(axes.flat, shapes.items()):
    ax.hist(values, bins=40, color="slateblue", edgecolor="white")
    ax.axvline(np.mean(values), color="red", ls="--", lw=1.2)
    ax.axvline(np.median(values), color="black", ls=":", lw=1.2)
    ax.set_title(name)
    ax.set_yticks([])
    print(f"  {name:<24} mean {np.mean(values):8.1f}  median {np.median(values):8.1f}")
fig.suptitle("Distribution shapes (red dashed = mean, black dotted = median)", fontsize=15, fontweight="bold")
save_and_show(fig, "06f_shapes_gallery.png")

# ---------------------------------------------------------------- 6. 2-D histogram
print("\n=== 6. hist2d: counts in 2-D cells ===")
x = rng.normal(0, 1, 20_000)
y = 0.6 * x + rng.normal(0, 0.8, 20_000)
fig, ax = plt.subplots(figsize=(7, 5.5))
h = ax.hist2d(x, y, bins=40, cmap="viridis")
fig.colorbar(h[3], ax=ax, label="points per cell")
ax.set_title("20,000 points: hist2d shows where they concentrate")
save_and_show(fig, "06g_hist2d.png")
