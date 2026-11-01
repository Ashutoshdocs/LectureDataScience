"""
10 - Basic Plot Types in Seaborn
--------------------------------
A tour of the most used Seaborn plots, grouped by purpose:
  Distribution : histplot, kdeplot
  Categorical  : countplot, barplot, boxplot, violinplot
  Relational   : lineplot
  Matrix       : heatmap (correlation)
"""

import matplotlib.pyplot as plt
import seaborn as sns
from common import get_students, get_monthly_sales, save_and_show

sns.set_theme(style="whitegrid")
df = get_students()
sales = get_monthly_sales()
order = ["Freshman", "Sophomore", "Junior", "Senior"]

fig, axes = plt.subplots(3, 3, figsize=(16, 13))

# Distribution plots
sns.histplot(data=df, x="score", kde=True, ax=axes[0, 0])
axes[0, 0].set_title("histplot (+ KDE)")

sns.kdeplot(data=df, x="score", hue="gender", fill=True, ax=axes[0, 1])
axes[0, 1].set_title("kdeplot by gender")

# Categorical plots
sns.countplot(data=df, x="grade_level", order=order, ax=axes[0, 2])
axes[0, 2].set_title("countplot (counts per category)")

sns.barplot(data=df, x="grade_level", y="score", order=order, ax=axes[1, 0])
axes[1, 0].set_title("barplot (mean + error bar)")

sns.boxplot(data=df, x="grade_level", y="score", hue="gender", order=order, ax=axes[1, 1])
axes[1, 1].set_title("boxplot (median, quartiles, outliers)")

sns.violinplot(data=df, x="gender", y="study_hours", ax=axes[1, 2])
axes[1, 2].set_title("violinplot (box + distribution shape)")

# Relational plot: needs long format -> melt wide sales table
long_sales = sales.melt(id_vars="Month", var_name="Category", value_name="Sales")
sns.lineplot(data=long_sales, x="Month", y="Sales", hue="Category", marker="o", ax=axes[2, 0])
axes[2, 0].set_title("lineplot (long-format data)")
axes[2, 0].tick_params(axis="x", rotation=45)

# Matrix plot: correlation heatmap
corr = df[["study_hours", "sleep_hours", "score"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=axes[2, 1])
axes[2, 1].set_title("heatmap (correlation)")

# Strip plot: every individual point per category
sns.stripplot(data=df, x="grade_level", y="score", order=order, alpha=0.6, ax=axes[2, 2])
axes[2, 2].set_title("stripplot (individual points)")

fig.suptitle("Basic Seaborn Plot Types", fontsize=18, fontweight="bold")
save_and_show(fig, "10_seaborn_plot_types.png")

# Pairplot: all pairwise relationships at once (figure-level function)
g = sns.pairplot(df, vars=["study_hours", "sleep_hours", "score"], hue="gender")
g.figure.suptitle("pairplot (every pair of numeric columns)", y=1.02)
save_and_show(g.figure, "10b_seaborn_pairplot.png")
