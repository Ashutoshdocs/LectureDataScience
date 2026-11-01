"""
09 - Introduction to Seaborn
----------------------------
Seaborn is built on top of Matplotlib. It works directly with pandas
DataFrames (pass column names), adds nicer defaults, and handles
grouping by category automatically with `hue`.
This demo makes the SAME chart in Matplotlib and Seaborn to compare.
"""

import matplotlib.pyplot as plt
import seaborn as sns
from common import get_students, save_and_show

df = get_students()

# Seaborn themes: "darkgrid", "whitegrid", "dark", "white", "ticks"
sns.set_theme(style="whitegrid", palette="deep")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

# --- Matplotlib: you loop over groups yourself ---
for gender in df["gender"].unique():
    sub = df[df["gender"] == gender]
    ax1.scatter(sub["study_hours"], sub["score"], label=gender, alpha=0.7)
ax1.set_title("Matplotlib (manual grouping)")
ax1.set_xlabel("study_hours")
ax1.set_ylabel("score")
ax1.legend()

# --- Seaborn: one line, hue does the grouping + legend ---
sns.scatterplot(data=df, x="study_hours", y="score", hue="gender", ax=ax2)
ax2.set_title("Seaborn (hue='gender')")

save_and_show(fig, "09a_mpl_vs_seaborn.png")

# --- Bonus: regression line + confidence band in one call ---
g = sns.lmplot(data=df, x="study_hours", y="score", hue="gender", height=5, aspect=1.4)
g.figure.suptitle("sns.lmplot: Scatter + Regression Line", y=1.02)
save_and_show(g.figure, "09b_seaborn_lmplot.png")
