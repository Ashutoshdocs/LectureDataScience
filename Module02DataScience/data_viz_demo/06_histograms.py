"""
06 - Histograms in Matplotlib
-----------------------------
A histogram groups numeric values into bins and counts them, showing the
SHAPE of a distribution. Covers: bins, edgecolor, mean line,
comparing two groups, and density.
"""

import matplotlib.pyplot as plt
from common import apply_style, get_students, save_and_show

apply_style()
df = get_students()

# --- 1. Basic histogram with a mean line ---
fig, ax = plt.subplots()
ax.hist(df["score"], bins=15, color="slateblue", edgecolor="white")
mean = df["score"].mean()
ax.axvline(mean, color="red", linestyle="--", label=f"Mean = {mean:.1f}")
ax.set_title("Distribution of Exam Scores")
ax.set_xlabel("Score")
ax.set_ylabel("Number of students")
ax.legend()
save_and_show(fig, "06a_histogram_basic.png")

# --- 2. Effect of bin count: too few hides detail, too many is noisy ---
fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=False)
for ax, bins in zip(axes, [5, 15, 50]):
    ax.hist(df["score"], bins=bins, edgecolor="white")
    ax.set_title(f"bins = {bins}")
save_and_show(fig, "06b_histogram_bins.png")

# --- 3. Overlapping histograms to compare groups ---
fig, ax = plt.subplots()
bins = range(0, 101, 5)  # same bins for both so they are comparable
for gender, color in [("Male", "tab:blue"), ("Female", "tab:pink")]:
    ax.hist(df.loc[df["gender"] == gender, "score"], bins=bins,
            alpha=0.6, label=gender, color=color, edgecolor="white")
ax.set_title("Scores by Gender (Overlapping)")
ax.set_xlabel("Score")
ax.set_ylabel("Count")
ax.legend()
save_and_show(fig, "06c_histogram_compare.png")
