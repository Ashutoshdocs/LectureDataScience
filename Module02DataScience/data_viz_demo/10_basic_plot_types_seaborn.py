import matplotlib.pyplot as plt
import seaborn as sns
from common import get_monthly_sales, get_students, save_and_show

sns.set_theme(style="whitegrid")
df = get_students()
sales = get_monthly_sales()
order = [
    "Freshman",
    "Sophomore",
    "Junior",
    "Senior",
]  # Establishes a custom categorical order for the charts

# Creates a large 3x3 uniform layout grid canvas
fig, axes = plt.subplots(3, 3, figsize=(16, 13))

# --- 1. Distribution Plots ---
# 'kde=True' overlays a smooth kernel density estimate curve directly onto the histogram bars
sns.histplot(data=df, x="score", kde=True, ax=axes[0, 0])
axes[0, 0].set_title("histplot (+ KDE)")

# Draws smoothed probability density curves; 'fill=True' colors the area underneath the curve
sns.kdeplot(data=df, x="score", hue="gender", fill=True, ax=axes[0, 1])
axes[0, 1].set_title("kdeplot by gender")

# --- 2. Categorical Plots ---
# A frequency bar chart that automatically aggregates and counts the number of rows per category
sns.countplot(data=df, x="grade_level", order=order, ax=axes[0, 2])
axes[0, 2].set_title("countplot (counts per category)")

# Plots categorical means; the thin vertical black lines at the top represent bootstrapped confidence interval error bars
sns.barplot(data=df, x="grade_level", y="score", order=order, ax=axes[1, 0])
axes[1, 0].set_title("barplot (mean + error bar)")

# Shows five-number summaries (min, 25%, median, 75%, max) broken down by gender across grade levels
sns.boxplot(
    data=df,
    x="grade_level",
    y="score",
    hue="gender",
    order=order,
    ax=axes[1, 1],
)
axes[1, 1].set_title("boxplot (median, quartiles, outliers)")

# Combines a mini internal boxplot with a mirrored continuous density curve on the sides
sns.violinplot(data=df, x="gender", y="study_hours", ax=axes[1, 2])
axes[1, 2].set_title("violinplot (box + distribution shape)")

# --- 3. Relational & Matrix Plots ---
# Reshapes wide-format columns into long-format key-value rows so Seaborn can process them cleanly
long_sales = sales.melt(
    id_vars="Month", var_name="Category", value_name="Sales"
)
sns.lineplot(
    data=long_sales,
    x="Month",
    y="Sales",
    hue="Category",
    marker="o",
    ax=axes[2, 0],
)
axes[2, 0].set_title("lineplot (long-format data)")
axes[2, 0].tick_params(axis="x", rotation=45)

# Matrix plot: correlation heatmap
corr = df[["study_hours", "sleep_hours", "score"]].corr()
# 'annot=True' prints r-values inside cells; 'vmin/vmax' fixes the color map bounds from -1 to 1
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=axes[2, 1])
axes[2, 1].set_title("heatmap (correlation)")

# Scatter plot variant where points are grouped into categorical vertical lanes
sns.stripplot(
    data=df, x="grade_level", y="score", order=order, alpha=0.6, ax=axes[2, 2]
)
axes[2, 2].set_title("stripplot (individual points)")

fig.suptitle("Basic Seaborn Plot Types", fontsize=18, fontweight="bold")
save_and_show(fig, "10_seaborn_plot_types.png")

# --- 4. Pairplot ---
# Figure-level plot generating a matrix of histograms along the diagonal and scatter plots everywhere else
g = sns.pairplot(df, vars=["study_hours", "sleep_hours", "score"], hue="gender")
g.figure.suptitle("pairplot (every pair of numeric columns)", y=1.02)
save_and_show(g.figure, "10b_seaborn_pairplot.png")
