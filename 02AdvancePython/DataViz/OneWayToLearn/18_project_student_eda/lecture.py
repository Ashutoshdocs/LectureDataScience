"""Lecture 18: Project: exploratory data analysis (EDA) of student performance with Seaborn.

Each step asks a question, draws the chart that answers it, and prints the finding."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from common import get_students, save_and_show  # noqa: E402

sns.set_theme(style="whitegrid", palette="colorblind", context="notebook")
ORDER = ["Freshman", "Sophomore", "Junior", "Senior"]
findings = []

# ---------------------------------------------------------------- 0. load + basic checks
df = get_students(n=400)
df["result"] = np.where(df["score"] >= 40, "Pass", "Fail")
df["study_band"] = pd.cut(df["study_hours"], [0, 3, 6, 10], labels=["0-3 h", "3-6 h", "6-10 h"], include_lowest=True)
print("=== Step 0. First look at the data ===")
print(df.head().to_string(index=False))
print("  shape:", df.shape, "| missing:", int(df.isna().sum().sum()))
print(df.describe().round(1).to_string())

# ---------------------------------------------------------------- 1. distributions of numeric columns
print("\n=== Step 1. How is each numeric variable distributed? ===")
fig, axes = plt.subplots(1, 3, figsize=(16, 4.3))
for ax, col, color in zip(axes, ["study_hours", "sleep_hours", "score"], sns.color_palette()[:3]):
    sns.histplot(data=df, x=col, kde=True, color=color, ax=ax)
    ax.axvline(df[col].mean(), color="black", ls="--", lw=1)
    ax.set_title(f"{col}: mean {df[col].mean():.1f}, median {df[col].median():.1f}")
fig.suptitle("Step 1: distributions", fontsize=15, fontweight="bold")
save_and_show(fig, "18_1_distributions.png")
findings.append(f"Study hours are spread evenly from 0-10; sleep is bell-shaped around {df['sleep_hours'].mean():.1f} h; "
                f"scores average {df['score'].mean():.1f} with {(df['result'] == 'Fail').mean():.0%} failing (< 40).")

# ---------------------------------------------------------------- 2. categorical composition
print("\n=== Step 2. Are groups balanced? ===")
fig, axes = plt.subplots(1, 2, figsize=(13, 4.3))
sns.countplot(data=df, x="grade_level", order=ORDER, hue="gender", ax=axes[0])
axes[0].set_title("Students per grade and gender")
for c in axes[0].containers:
    axes[0].bar_label(c, fontsize=9)
sns.countplot(data=df, x="result", hue="gender", ax=axes[1])
axes[1].set_title("Pass / fail by gender")
fig.suptitle("Step 2: group sizes", fontsize=15, fontweight="bold")
save_and_show(fig, "18_2_group_sizes.png")
counts = df["grade_level"].value_counts()
findings.append(f"Grades are roughly balanced ({counts.min()}-{counts.max()} students each); gender split {df['gender'].value_counts().to_dict()}.")

# ---------------------------------------------------------------- 3. relationships
print("\n=== Step 3. Which variables relate to score? ===")
corr = df[["study_hours", "sleep_hours", "score"]].corr()
print(corr.round(2).to_string())
g = sns.pairplot(df, vars=["study_hours", "sleep_hours", "score"], hue="result", hue_order=["Fail", "Pass"],
                 corner=True, height=2.6, plot_kws={"s": 18, "alpha": 0.7})
g.figure.suptitle("Step 3: relationships (colour = pass/fail)", y=1.02, fontsize=15, fontweight="bold")
save_and_show(g.figure, "18_3_pairplot.png")
fig, ax = plt.subplots(figsize=(5.5, 4.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", vmin=-1, vmax=1, square=True, ax=ax)
ax.set_title("Correlation matrix")
save_and_show(fig, "18_3b_correlation.png")
findings.append(f"Study hours are the strongest driver of score (r = {corr.loc['study_hours', 'score']:.2f}); "
                f"sleep has a weak positive link (r = {corr.loc['sleep_hours', 'score']:.2f}).")

# ---------------------------------------------------------------- 4. the main relationship in detail
print("\n=== Step 4. How much does each study hour add? ===")
slope, intercept = np.polyfit(df["study_hours"], df["score"], 1)
g = sns.lmplot(data=df, x="study_hours", y="score", hue="gender", height=5, aspect=1.4, scatter_kws={"alpha": 0.5})
for ax in g.axes.flat:
    ax.axhline(40, color="red", ls="--", lw=1)
    ax.text(0.2, 41.5, "pass mark", color="red")
    pass_hours = (40 - intercept) / slope
    ax.axvline(pass_hours, color="gray", ls=":", lw=1)
    ax.text(pass_hours + 0.1, 15, f"~{pass_hours:.1f} h/day\nto reach 40 on average", color="gray")
g.figure.suptitle(f"Step 4: each extra study hour adds ~{slope:.1f} points (similar for both genders)", y=1.03,
                  fontsize=14, fontweight="bold")
save_and_show(g.figure, "18_4_study_vs_score.png")
by_gender = {gname: float(np.polyfit(gdf["study_hours"], gdf["score"], 1)[0]) for gname, gdf in df.groupby("gender")}
print("  slope by gender:", {k: round(v, 2) for k, v in by_gender.items()})
findings.append(f"Each extra study hour adds ~{slope:.1f} points; on average a student needs ~{(40 - intercept) / slope:.1f} h/day "
                f"to pass. The slope is nearly the same for both genders ({', '.join(f'{k} {v:.1f}' for k, v in by_gender.items())}).")

# ---------------------------------------------------------------- 5. compare groups
print("\n=== Step 5. Do grades or genders differ? ===")
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
sns.boxplot(data=df, x="grade_level", y="score", order=ORDER, hue="gender", ax=axes[0])
axes[0].set_title("Score by grade and gender")
sns.violinplot(data=df, x="study_band", y="score", hue="study_band", palette="crest", inner="quart", legend=False, ax=axes[1])
sns.stripplot(data=df, x="study_band", y="score", color="black", size=2.5, alpha=0.4, ax=axes[1])
axes[1].axhline(40, color="red", ls="--", lw=1)
axes[1].set_title("Score by study band (red = pass mark)")
fig.suptitle("Step 5: group comparisons", fontsize=15, fontweight="bold")
save_and_show(fig, "18_5_group_comparisons.png")
grade_means = df.groupby("grade_level")["score"].mean().loc[ORDER]
band_pass = df.groupby("study_band", observed=True)["result"].apply(lambda s: (s == "Pass").mean())
print("  mean score by grade:", grade_means.round(1).to_dict())
print("  pass rate by study band:", band_pass.round(2).to_dict())
findings.append(f"Grade level barely matters (means {grade_means.min():.0f}-{grade_means.max():.0f}); "
                f"study band matters a lot: pass rate {band_pass.iloc[0]:.0%} for 0-3 h vs {band_pass.iloc[-1]:.0%} for 6-10 h.")

# ---------------------------------------------------------------- 6. two factors together
print("\n=== Step 6. Study and sleep together ===")
df["sleep_band"] = pd.cut(df["sleep_hours"], [0, 6, 8, 12], labels=["< 6 h", "6-8 h", "> 8 h"])
table = df.pivot_table(index="sleep_band", columns="study_band", values="score", aggfunc="mean", observed=True)
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
sns.heatmap(table, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={"label": "mean score"}, ax=axes[0])
axes[0].set_title("Mean score by sleep x study band")
sns.scatterplot(data=df, x="study_hours", y="score", hue="sleep_hours", palette="viridis", size="sleep_hours",
                sizes=(10, 120), ax=axes[1])
axes[1].set_title("Colour/size = sleep hours")
axes[1].legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8, title="sleep")
fig.suptitle("Step 6: combining factors", fontsize=15, fontweight="bold")
save_and_show(fig, "18_6_two_factors.png")
print(table.round(1).to_string())
gaps = (table.iloc[-1] - table.iloc[0])
findings.append(f"Sleep adds on top of study: in every study band, > 8 h sleepers outscore < 6 h sleepers by "
                f"{gaps.min():.0f}-{gaps.max():.0f} points (6-10 h band: {table.iloc[-1, -1]:.0f} vs {table.iloc[0, -1]:.0f}).")

# ---------------------------------------------------------------- 7. one summary figure
print("\n=== Step 7. One-page summary for a presentation ===")
fig, ax = plt.subplot_mosaic([["main", "main", "pass"], ["main", "main", "grade"]], figsize=(15, 8), layout="constrained")
sns.regplot(data=df, x="study_hours", y="score", ax=ax["main"], scatter_kws={"alpha": 0.4, "s": 18}, line_kws={"color": "red"})
ax["main"].axhline(40, color="gray", ls="--")
ax["main"].set_title(f"Study time is the #1 driver: +{slope:.1f} points per hour", loc="left", fontweight="bold")
sns.barplot(x=band_pass.index.astype(str), y=band_pass.values * 100, hue=band_pass.index.astype(str), palette="crest",
            legend=False, ax=ax["pass"])
for c in ax["pass"].containers:
    ax["pass"].bar_label(c, fmt="%.0f%%")
ax["pass"].set_ylim(0, 115)
ax["pass"].set_title("Pass rate by study band", loc="left")
ax["pass"].set_ylabel("%")
sns.pointplot(data=df, x="grade_level", y="score", order=ORDER, ax=ax["grade"])
ax["grade"].set_ylim(30, 80)
ax["grade"].set_title("Grade level hardly matters", loc="left")
fig.suptitle("Student performance: key findings", fontsize=18, fontweight="bold")
save_and_show(fig, "18_7_summary.png")

print("\n=== FINDINGS ===")
for i, f in enumerate(findings, start=1):
    print(f"  {i}. {f}")
print("  Caveat: observational (generated) data. These are associations, not proof of cause.")
