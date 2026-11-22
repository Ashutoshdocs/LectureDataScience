"""Lecture 14: heatmap (correlation, pivot, crosstab, mask), clustermap, pairplot, PairGrid, jointplot, FacetGrid."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from common import get_regional_sales, get_restaurant_bills, get_students, save_and_show  # noqa: E402

sns.set_theme(style="whitegrid")
df = get_students()
bills = get_restaurant_bills()
reg = get_regional_sales()

# ---------------------------------------------------------------- 1. correlation heatmap
print("=== 1. Correlation heatmap (full and masked lower triangle) ===")
num = bills[["total_bill", "tip", "size"]].assign(tip_pct=bills["tip"] / bills["total_bill"] * 100)
corr = num.corr()
print(corr.round(2).to_string())
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, square=True, ax=axes[0])
axes[0].set_title("full matrix (each pair twice)")
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, square=True,
            linewidths=1, ax=axes[1])
axes[1].set_title("mask=upper triangle: each pair once")
save_and_show(fig, "14a_correlation_heatmap.png")

# ---------------------------------------------------------------- 2. pivot + crosstab heatmaps
print("\n=== 2. Pivot-table and crosstab heatmaps ===")
pivot = reg.pivot_table(index="region", columns="quarter", values="sales", aggfunc="sum")
gap = (reg.assign(gap=reg["sales"] - reg["target"])
          .pivot_table(index="region", columns="quarter", values="gap", aggfunc="sum"))
counts = pd.crosstab(bills["day"], bills["time"]).loc[["Thu", "Fri", "Sat", "Sun"]]
fig, axes = plt.subplots(1, 3, figsize=(17, 4.5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={"label": "sales (lakh)"}, ax=axes[0])
axes[0].set_title("Sales by region x quarter (sequential)")
sns.heatmap(gap, annot=True, fmt="+.0f", cmap="RdYlGn", center=0, ax=axes[1])
axes[1].set_title("Sales minus target (diverging, center=0)")
sns.heatmap(counts, annot=True, fmt="d", cmap="Purples", ax=axes[2])
axes[2].set_title("crosstab: bills per day x time")
print("  regions below target in some quarter:", gap[gap.lt(0).any(axis=1)].index.tolist())
save_and_show(fig, "14b_pivot_crosstab_heatmaps.png")

# ---------------------------------------------------------------- 3. clustermap
print("\n=== 3. clustermap groups similar rows/columns ===")
rng = np.random.default_rng(0)
profiles = pd.DataFrame(
    np.r_[rng.normal([8, 7, 2, 1, 3], 0.8, (6, 5)), rng.normal([2, 1, 8, 7, 3], 0.8, (6, 5))],
    columns=["laptops", "phones", "groceries", "household", "books"],
    index=[f"store {i}" for i in rng.permutation(12)])
g = sns.clustermap(profiles, cmap="viridis", standard_scale=1, figsize=(7, 6))
g.figure.suptitle("clustermap: two store types emerge", y=1.02)
save_and_show(g.figure, "14c_clustermap.png")

# ---------------------------------------------------------------- 4. pairplot (your original) + corner
print("\n=== 4. pairplot ===")
g = sns.pairplot(df, vars=["study_hours", "sleep_hours", "score"], hue="gender", corner=True, height=2.6)
g.figure.suptitle("pairplot(corner=True): every pair of numeric columns", y=1.02)
save_and_show(g.figure, "14d_pairplot.png")

# ---------------------------------------------------------------- 5. PairGrid custom
print("\n=== 5. PairGrid: different plots above, below and on the diagonal ===")
g = sns.PairGrid(df, vars=["study_hours", "sleep_hours", "score"], height=2.6)
g.map_lower(sns.scatterplot, s=12, alpha=0.6)
g.map_upper(sns.kdeplot, fill=True, cmap="Blues")
g.map_diag(sns.histplot, kde=True, color="tab:purple")
g.figure.suptitle("PairGrid: scatter (lower), KDE (upper), hist (diagonal)", y=1.02)
save_and_show(g.figure, "14e_pairgrid.png")

# ---------------------------------------------------------------- 6. jointplot kinds
print("\n=== 6. jointplot: relationship + marginal distributions ===")
for kind in ["reg", "hex", "kde"]:
    g = sns.jointplot(data=df, x="study_hours", y="score", kind=kind, height=5,
                      color={"reg": "tab:blue", "hex": "tab:green", "kde": "tab:purple"}[kind])
    g.figure.suptitle(f"jointplot(kind='{kind}')", y=1.02)
    save_and_show(g.figure, f"14f_jointplot_{kind}.png")

# ---------------------------------------------------------------- 7. FacetGrid
print("\n=== 7. FacetGrid: map any function onto a grid ===")
g = sns.FacetGrid(df, row="gender", col="grade_level", col_order=["Freshman", "Sophomore", "Junior", "Senior"],
                  height=2.6, aspect=1.1, margin_titles=True)
g.map_dataframe(sns.histplot, x="score", binwidth=10, color="tab:blue")
g.refline(x=df["score"].mean(), color="red", ls="--")
g.set_axis_labels("Score", "Students")
g.set_titles(col_template="{col_name}", row_template="{row_name}")
g.figure.suptitle("FacetGrid(row='gender', col='grade_level') + refline at the overall mean", y=1.03)
print("  grid shape:", g.axes.shape)
save_and_show(g.figure, "14g_facetgrid.png")
