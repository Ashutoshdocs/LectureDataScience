"""Lecture 12: countplot, barplot (error bars), pointplot, boxplot, violinplot, strip/swarm, box+strip combo, catplot,
and why means can hide distributions."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from common import get_restaurant_bills, get_students, save_and_show  # noqa: E402

sns.set_theme(style="whitegrid")
df = get_students()
bills = get_restaurant_bills()
order = ["Freshman", "Sophomore", "Junior", "Senior"]
days = ["Thu", "Fri", "Sat", "Sun"]

# ---------------------------------------------------------------- 1. the 3 families at a glance (your original grid, extended)
print("=== 1. Estimates, summaries and every observation ===")
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
sns.countplot(data=df, x="grade_level", order=order, ax=axes[0, 0])
axes[0, 0].set_title("countplot: rows per category")
sns.barplot(data=df, x="grade_level", y="score", order=order, ax=axes[0, 1])
axes[0, 1].set_title("barplot: mean + 95% CI")
sns.pointplot(data=df, x="grade_level", y="score", hue="gender", order=order, dodge=0.2, ax=axes[0, 2])
axes[0, 2].set_title("pointplot: compare hue across categories")
sns.boxplot(data=df, x="grade_level", y="score", hue="gender", order=order, ax=axes[1, 0])
axes[1, 0].set_title("boxplot: median, quartiles, outliers")
sns.violinplot(data=df, x="gender", y="study_hours", inner="quart", ax=axes[1, 1])
axes[1, 1].set_title("violinplot: shape + quartiles")
sns.stripplot(data=df, x="grade_level", y="score", order=order, alpha=0.6, ax=axes[1, 2])
axes[1, 2].set_title("stripplot: every student")
fig.suptitle("Seaborn categorical plots", fontsize=17, fontweight="bold")
print("  counts per grade:", df["grade_level"].value_counts().loc[order].to_dict())
save_and_show(fig, "12a_categorical_overview.png")

# ---------------------------------------------------------------- 2. error bars mean different things
print("\n=== 2. barplot error bars: CI vs SD vs SE ===")
fig, axes = plt.subplots(1, 3, figsize=(15, 4.3), sharey=True)
for ax, eb, title in zip(axes, [("ci", 95), "sd", "se"], ["95% CI of the mean", "standard deviation", "standard error"]):
    sns.barplot(data=bills, x="day", y="tip", order=days, errorbar=eb, capsize=0.2, ax=ax)
    ax.set_title(f"errorbar={eb!r}\n({title})")
print("  SD describes how spread out tips are; CI/SE describe how precisely we know the MEAN")
print("  mean tip by day:", bills.groupby("day")["tip"].mean().loc[days].round(2).to_dict())
save_and_show(fig, "12b_barplot_errorbars.png")

# ---------------------------------------------------------------- 3. means hide distributions
print("\n=== 3. Same mean, very different data ===")
rng = np.random.default_rng(4)
demo = pd.DataFrame({"group": ["A"] * 100 + ["B"] * 100 + ["C"] * 100,
                     "value": np.r_[rng.normal(50, 3, 100), np.r_[rng.normal(35, 3, 50), rng.normal(65, 3, 50)],
                                    rng.uniform(20, 80, 100)]})
demo["value"] = demo["value"] - demo.groupby("group")["value"].transform("mean") + 50     # make every mean exactly 50
fig, axes = plt.subplots(1, 4, figsize=(18, 4.3), sharey=True)
sns.barplot(data=demo, x="group", y="value", ax=axes[0])
axes[0].set_title("barplot: all look the same")
sns.boxplot(data=demo, x="group", y="value", ax=axes[1])
axes[1].set_title("boxplot: spreads differ")
sns.violinplot(data=demo, x="group", y="value", ax=axes[2])
axes[2].set_title("violinplot: B is bimodal!")
sns.swarmplot(data=demo, x="group", y="value", size=3, ax=axes[3])
axes[3].set_title("swarmplot: the raw truth")
print("  group means:", demo.groupby("group")["value"].mean().round(1).to_dict())
save_and_show(fig, "12c_means_hide_shape.png")

# ---------------------------------------------------------------- 4. box + strip combo, split violin
print("\n=== 4. boxplot + stripplot, and a split violin ===")
fig, axes = plt.subplots(1, 2, figsize=(15, 5))
sns.boxplot(data=bills, x="day", y="total_bill", order=days, color="lightsteelblue", fliersize=0, ax=axes[0])
sns.stripplot(data=bills, x="day", y="total_bill", order=days, color="black", size=3, alpha=0.6, ax=axes[0])
axes[0].set_title("box (summary) + strip (raw points)")
sns.violinplot(data=bills, x="day", y="total_bill", order=days, hue="time", split=True, inner="quart", ax=axes[1])
axes[1].set_title("violinplot(hue='time', split=True)")
save_and_show(fig, "12d_box_strip_split_violin.png")

# ---------------------------------------------------------------- 5. horizontal + boxenplot
print("\n=== 5. Horizontal orientation and boxenplot for bigger data ===")
big = pd.DataFrame({"region": np.repeat(["North", "South", "East", "West"], 2000),
                    "delivery_days": np.r_[rng.gamma(2, 1.5, 2000), rng.gamma(3, 1.2, 2000),
                                           rng.gamma(2.5, 1.0, 2000), rng.gamma(4, 1.3, 2000)]})
fig, axes = plt.subplots(1, 2, figsize=(15, 4.5))
sns.boxplot(data=big, y="region", x="delivery_days", ax=axes[0])
axes[0].set_title("boxplot (horizontal): many 'outliers' in skewed data")
sns.boxenplot(data=big, y="region", x="delivery_days", ax=axes[1])
axes[1].set_title("boxenplot: more quantiles, better for large skewed data")
save_and_show(fig, "12e_horizontal_boxen.png")

# ---------------------------------------------------------------- 6. catplot (figure-level)
print("\n=== 6. catplot: facets ===")
g = sns.catplot(data=bills, x="day", y="tip", hue="smoker", col="time", kind="point", order=days,
                dodge=0.2, height=4, aspect=1.2)
g.figure.suptitle("catplot(kind='point', col='time')", y=1.04)
save_and_show(g.figure, "12f_catplot.png")
