import matplotlib.pyplot as plt
from common import apply_style, get_students, save_and_show

apply_style()
df = get_students()  # Fetches a DataFrame containing student metrics (e.g., score, gender)

# --- 1. Basic histogram with a mean line ---
fig, ax = plt.subplots()
# Groups numerical scores into 15 equal intervals and counts the occurrences in each interval
ax.hist(df["score"], bins=15, color="slateblue", edgecolor="white")

mean = df["score"].mean()  # Calculates the average score across the entire dataset
# Draws a continuous vertical helper line across the entire plot height at the mean coordinate position
ax.axvline(mean, color="red", linestyle="--", label=f"Mean = {mean:.1f}")

ax.set_title("Distribution of Exam Scores")
ax.set_xlabel("Score")
ax.set_ylabel("Number of students")
ax.legend()
save_and_show(fig, "06a_histogram_basic.png")

# --- 2. Effect of bin count: too few hides detail, too many is noisy ---
# Generates a row of 3 subplots to explicitly test how bin width changes layout clarity
fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=False)
for ax, bins in zip(axes, [5, 15, 50]):
    ax.hist(df["score"], bins=bins, edgecolor="white")
    ax.set_title(f"bins = {bins}")
save_and_show(fig, "06b_histogram_bins.png")

# --- 3. Overlapping histograms to compare groups ---
fig, ax = plt.subplots()
bins = range(
    0, 101, 5
)  # Explicitly defines uniform bin boundary marks from 0 to 100 in steps of 5

# Loops through categories to overlay separate data subsets onto the exact same plot coordinates
for gender, color in [("Male", "tab:blue"), ("Female", "tab:pink")]:
    # Filters rows matching the target gender, extracts only the 'score' column, and plots it
    ax.hist(
        df.loc[df["gender"] == gender, "score"],
        bins=bins,
        alpha=0.6,  # 60% opacity allows the bars underneath to show through where groups overlap
        label=gender,
        color=color,
        edgecolor="white",
    )
ax.set_title("Scores by Gender (Overlapping)")
ax.set_xlabel("Score")
ax.set_ylabel("Count")
ax.legend()
save_and_show(fig, "06c_histogram_compare.png")
