import matplotlib.pyplot as plt
import seaborn as sns
from common import get_students, save_and_show

df = get_students()

# Seaborn themes: "darkgrid", "whitegrid", "dark", "white", "ticks"
# Sets global style parameters, including a clean background grid and a cohesive color palette ('deep')
sns.set_theme(style="whitegrid", palette="deep")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# --- Matplotlib: you loop over groups yourself ---
# Loops through each unique value in the 'gender' column (e.g., 'Male', 'Female')
for gender in df["gender"].unique():
    sub = df[df["gender"] == gender]  # Manually slices out a subset DataFrame for this specific gender
    ax1.scatter(
        sub["study_hours"], sub["score"], label=gender, alpha=0.7
    )  # Plots the isolated subset
ax1.set_title("Matplotlib (manual grouping)")
ax1.set_xlabel("study_hours")
ax1.set_ylabel("score")
ax1.legend()

# --- Seaborn: one line, hue does the grouping + legend ---
# Passes the whole DataFrame, selects column strings for axes, and delegates color segmentation to 'hue'
sns.scatterplot(data=df, x="study_hours", y="score", hue="gender", ax=ax2)
ax2.set_title("Seaborn (hue='gender')")

save_and_show(fig, "09a_mpl_vs_seaborn.png")

# --- Bonus: regression line + confidence band in one call ---
# 'lmplot' automatically fits a linear regression line along with a shaded 95% confidence interval band
g = sns.lmplot(
    data=df, x="study_hours", y="score", hue="gender", height=5, aspect=1.4
)
# 'lmplot' returns a Seaborn FacetGrid object; we access its internal figure canvas to set a global title
g.figure.suptitle("sns.lmplot: Scatter + Regression Line", y=1.02)
save_and_show(g.figure, "09b_seaborn_lmplot.png")
