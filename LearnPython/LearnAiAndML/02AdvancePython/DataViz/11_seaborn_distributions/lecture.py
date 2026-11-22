"""Lecture 11: histplot (kde, multiple, stat), kdeplot (bw_adjust, cut, 2-D), ecdfplot, rugplot, displot."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import seaborn as sns  # noqa: E402
from common import get_restaurant_bills, get_students, save_and_show  # noqa: E402

sns.set_theme(style="whitegrid")
df = get_students()
bills = get_restaurant_bills()

# ---------------------------------------------------------------- 1. histplot basics
print("=== 1. histplot with kde, and stat options ===")
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
sns.histplot(data=df, x="score", kde=True, ax=axes[0])
axes[0].set_title("histplot(kde=True)")
sns.histplot(data=df, x="score", binwidth=5, stat="percent", color="tab:green", ax=axes[1])
axes[1].set_title("binwidth=5, stat='percent'")
sns.histplot(data=bills, x="total_bill", y="tip", bins=20, cbar=True, ax=axes[2])
axes[2].set_title("x + y: a 2-D histogram")
save_and_show(fig, "11a_histplot_basics.png")

# ---------------------------------------------------------------- 2. multiple= for groups
print("\n=== 2. hue + multiple: layer, stack, dodge, fill ===")
fig, axes = plt.subplots(1, 4, figsize=(18, 4.2), sharey=False)
for ax, mode in zip(axes, ["layer", "stack", "dodge", "fill"]):
    sns.histplot(data=df, x="score", hue="gender", multiple=mode, binwidth=10, ax=ax, legend=(mode == "fill"))
    ax.set_title(f"multiple='{mode}'")
save_and_show(fig, "11b_histplot_multiple.png")

# ---------------------------------------------------------------- 3. kdeplot: bandwidth and cut
print("\n=== 3. kdeplot: bandwidth controls smoothness; cut=0 keeps it in range ===")
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
sns.histplot(data=df, x="score", stat="density", color="lightgray", ax=axes[0])
for bw, color in [(0.2, "tab:red"), (1, "tab:blue"), (3, "tab:green")]:
    sns.kdeplot(data=df, x="score", bw_adjust=bw, color=color, lw=2, label=f"bw_adjust={bw}", ax=axes[0])
axes[0].legend()
axes[0].set_title("too wiggly / about right / over-smoothed")
sns.kdeplot(data=bills, x="tip", fill=True, ax=axes[1], label="default (extends past the data)")
sns.kdeplot(data=bills, x="tip", fill=True, cut=0, ax=axes[1], label="cut=0")
axes[1].axvline(bills["tip"].min(), color="black", ls=":", lw=1)
axes[1].legend()
axes[1].set_title("tips can't be below the minimum: use cut=0")
save_and_show(fig, "11c_kde_bandwidth_cut.png")

# ---------------------------------------------------------------- 4. comparing groups: kde vs ecdf
print("\n=== 4. Comparing groups: KDE (shape) and ECDF (exact proportions) ===")
order = ["Freshman", "Sophomore", "Junior", "Senior"]
fig, axes = plt.subplots(1, 2, figsize=(14, 4.8))
sns.kdeplot(data=df, x="score", hue="grade_level", hue_order=order, common_norm=False, fill=True, alpha=0.2, ax=axes[0])
axes[0].set_title("kdeplot(hue=, common_norm=False)")
sns.ecdfplot(data=df, x="score", hue="grade_level", hue_order=order, ax=axes[1])
axes[1].axvline(50, color="gray", ls="--")
axes[1].axhline(0.5, color="gray", ls=":")
axes[1].set_title("ecdfplot: read 'share scoring <= x'")
below50 = (df["score"] < 50).groupby(df["grade_level"]).mean().loc[order]
print("  share scoring below 50 by grade:", below50.round(2).to_dict())
save_and_show(fig, "11d_kde_vs_ecdf.png")

# ---------------------------------------------------------------- 5. rug + 2-D kde
print("\n=== 5. rugplot and 2-D KDE contours ===")
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
small = df.sample(40, random_state=1)
sns.kdeplot(data=small, x="score", fill=True, ax=axes[0])
sns.rugplot(data=small, x="score", height=0.06, color="black", ax=axes[0])
axes[0].set_title("kde + rugplot (40 students: every value visible)")
sns.kdeplot(data=df, x="study_hours", y="score", fill=True, levels=8, cmap="mako", thresh=0.05, ax=axes[1])
sns.scatterplot(data=df, x="study_hours", y="score", s=10, color="white", edgecolor="black", ax=axes[1])
axes[1].set_title("2-D KDE contours + points")
save_and_show(fig, "11e_rug_and_2d_kde.png")

# ---------------------------------------------------------------- 6. displot (figure-level)
print("\n=== 6. displot: facets with col= ===")
g = sns.displot(data=bills, x="total_bill", col="day", col_order=["Thu", "Fri", "Sat", "Sun"], hue="time",
                kind="hist", binwidth=5, height=3.2, aspect=1)
g.figure.suptitle("displot(col='day', hue='time')", y=1.04)
print("  bill medians by day:", bills.groupby("day")["total_bill"].median().round(1).to_dict())
save_and_show(g.figure, "11f_displot_facets.png")

# ---------------------------------------------------------------- 7. skewed data: log scale
print("\n=== 7. Skewed data: log_scale=True ===")
rng = np.random.default_rng(0)
incomes = rng.lognormal(10.5, 0.7, 3000)
fig, axes = plt.subplots(1, 2, figsize=(13, 4.2))
sns.histplot(x=incomes, ax=axes[0], color="tab:purple")
axes[0].set_title("incomes: long right tail")
sns.histplot(x=incomes, log_scale=True, ax=axes[1], color="tab:purple")
axes[1].set_title("log_scale=True: symmetric on a log axis")
save_and_show(fig, "11g_log_scale.png")
