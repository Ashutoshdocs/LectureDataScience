"""Lecture 10: Seaborn intro: Matplotlib vs Seaborn, semantic mappings, long vs wide data, axes- vs figure-level,
mixing Seaborn with Matplotlib."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import seaborn as sns  # noqa: E402
from common import get_monthly_sales, get_students, save_and_show  # noqa: E402

df = get_students()
sales = get_monthly_sales()
sns.set_theme(style="whitegrid", palette="deep")

# ---------------------------------------------------------------- 1. matplotlib loop vs seaborn hue (your original demo)
print("=== 1. Manual grouping (Matplotlib) vs hue= (Seaborn) ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))
for gender in df["gender"].unique():
    sub = df[df["gender"] == gender]
    ax1.scatter(sub["study_hours"], sub["score"], label=gender, alpha=0.7)
ax1.set_title("Matplotlib (manual grouping)")
ax1.set_xlabel("study_hours")
ax1.set_ylabel("score")
ax1.legend()
returned = sns.scatterplot(data=df, x="study_hours", y="score", hue="gender", ax=ax2)
ax2.set_title("Seaborn (hue='gender')")
print("  sns.scatterplot returned a", type(returned).__name__, "-> it is the same object as ax2:", returned is ax2)
save_and_show(fig, "10a_mpl_vs_seaborn.png")

# ---------------------------------------------------------------- 2. semantic mappings
print("\n=== 2. hue + style + size on one chart ===")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x="study_hours", y="score", hue="grade_level", style="gender", size="sleep_hours",
                sizes=(20, 200), alpha=0.75, ax=ax)
ax.set_title("x, y = position | hue = grade | style = gender | size = sleep")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=9)
save_and_show(fig, "10b_semantic_mappings.png")

# ---------------------------------------------------------------- 3. wide vs long
print("\n=== 3. Wide vs long (tidy) data ===")
long_sales = sales.melt(id_vars="Month", var_name="Category", value_name="Sales")
print("  wide:", sales.shape, list(sales.columns))
print("  long:", long_sales.shape, list(long_sales.columns))
print(long_sales.head(3).to_string(index=False))
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 4.8))
sns.lineplot(data=sales.set_index("Month"), ax=ax1, markers=True)          # wide works for simple cases
ax1.set_title("Wide DataFrame: one line per column")
sns.lineplot(data=long_sales, x="Month", y="Sales", hue="Category", style="Category", markers=True, ax=ax2)
ax2.set_title("Long DataFrame + hue/style: full control")
for ax in (ax1, ax2):
    ax.tick_params(axis="x", rotation=45)
save_and_show(fig, "10c_wide_vs_long.png")
back = long_sales.pivot(index="Month", columns="Category", values="Sales")
print("  pivot back to wide:", back.shape)

# ---------------------------------------------------------------- 4. figure-level: lmplot (your bonus) and relplot
print("\n=== 4. Figure-level functions make their own figure ===")
g = sns.lmplot(data=df, x="study_hours", y="score", hue="gender", height=5, aspect=1.4)
g.figure.suptitle("sns.lmplot: scatter + regression line + 95% confidence band", y=1.02)
print("  lmplot returned a", type(g).__name__)
save_and_show(g.figure, "10d_lmplot.png")

g = sns.relplot(data=df, x="study_hours", y="score", hue="gender", col="grade_level", col_wrap=2,
                col_order=["Freshman", "Sophomore", "Junior", "Senior"], height=3.5, aspect=1.3)
g.figure.suptitle("relplot(col='grade_level', col_wrap=2): one panel per grade", y=1.02)
g.set_axis_labels("Study hours", "Score")
print("  relplot axes grid shape:", g.axes.shape)
save_and_show(g.figure, "10e_relplot_facets.png")

# ---------------------------------------------------------------- 5. Seaborn + Matplotlib together
print("\n=== 5. Draw with Seaborn, finish with Matplotlib ===")
fig, ax = plt.subplots(figsize=(9, 5.5))
sns.regplot(data=df, x="study_hours", y="score", scatter_kws={"alpha": 0.5}, line_kws={"color": "red"}, ax=ax)
top = df.loc[df["score"].idxmax()]
ax.annotate(f"top score {top['score']:.0f}", xy=(top["study_hours"], top["score"]), xytext=(4, 97),
            arrowprops=dict(arrowstyle="->"))
ax.axhline(40, color="gray", ls="--")
ax.text(0.1, 41, "pass mark", color="gray")
ax.set_title("sns.regplot + Matplotlib annotate/axhline", loc="left")
sns.despine(ax=ax)
save_and_show(fig, "10f_seaborn_plus_matplotlib.png")
