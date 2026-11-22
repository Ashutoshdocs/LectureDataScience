"""Lecture 13: scatterplot, lineplot (aggregation, bands, units), relplot facets, regplot (order, lowess),
lmplot, residplot."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402
from common import get_daily_visits, get_monthly_sales, get_restaurant_bills, save_and_show  # noqa: E402

sns.set_theme(style="whitegrid")
bills = get_restaurant_bills()
visits = get_daily_visits()

# ---------------------------------------------------------------- 1. scatterplot
print("=== 1. scatterplot with hue and size ===")
fig, ax = plt.subplots(figsize=(9, 5.5))
sns.scatterplot(data=bills, x="total_bill", y="tip", hue="time", size="size", sizes=(20, 160), alpha=0.7, ax=ax)
ax.set_title("Tip vs total bill (hue = time, size = party size)")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
print(f"  correlation tip~bill: {bills['tip'].corr(bills['total_bill']):.2f}")
save_and_show(fig, "13a_scatterplot.png")

# ---------------------------------------------------------------- 2. lineplot aggregation
print("\n=== 2. lineplot aggregates repeated x values (mean + 95% CI) ===")
visits["week"] = visits["date"].dt.isocalendar().week.astype(int)
visits["weekday"] = visits["date"].dt.day_name().str[:3]
fig, axes = plt.subplots(1, 3, figsize=(17, 4.5))
sns.lineplot(data=visits, x="week", y="visits", ax=axes[0])
axes[0].set_title("7 days per week -> mean + 95% CI band")
sns.lineplot(data=visits, x="week", y="visits", errorbar="sd", estimator="median", color="tab:green", ax=axes[1])
axes[1].set_title("estimator='median', errorbar='sd'")
sns.lineplot(data=visits, x="week", y="visits", units="weekday", estimator=None, hue="weekday",
             hue_order=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], lw=1, ax=axes[2])
axes[2].set_title("units='weekday', estimator=None: one line each")
axes[2].legend(ncols=2, fontsize=8)
print("  rows per week:", visits.groupby("week").size().iloc[1:4].tolist(), "-> aggregation needed")
save_and_show(fig, "13b_lineplot_aggregation.png")

# ---------------------------------------------------------------- 3. lineplot with hue + style on long data (your original)
print("\n=== 3. lineplot on long-format data (hue + style + markers) ===")
long_sales = get_monthly_sales().melt(id_vars="Month", var_name="Category", value_name="Sales")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=long_sales, x="Month", y="Sales", hue="Category", style="Category", markers=True, dashes=False, ax=ax)
ax.set_title("lineplot (long-format data)")
save_and_show(fig, "13c_lineplot_long.png")

# ---------------------------------------------------------------- 4. relplot facets
print("\n=== 4. relplot: the same chart per group ===")
g = sns.relplot(data=bills, x="total_bill", y="tip", col="day", col_order=["Thu", "Fri", "Sat", "Sun"],
                hue="smoker", height=3.4, aspect=0.95)
g.figure.suptitle("relplot(col='day', hue='smoker')", y=1.04)
save_and_show(g.figure, "13d_relplot_facets.png")

# ---------------------------------------------------------------- 5. regplot fits
print("\n=== 5. regplot: straight, polynomial, lowess ===")
rng = np.random.default_rng(2)
hours = rng.uniform(0, 12, 150)
practice = pd.DataFrame({"hours": hours, "performance": 20 + 14 * hours - 0.9 * hours ** 2 + rng.normal(0, 6, 150)})
fig, axes = plt.subplots(1, 3, figsize=(16, 4.6), sharey=True)
for ax, kwargs, title in zip(axes, [{}, {"order": 2}, {"lowess": True}],
                             ["straight line (order=1)", "order=2", "lowess=True (no shape assumed)"]):
    try:
        sns.regplot(data=practice, x="hours", y="performance", scatter_kws={"alpha": 0.4}, line_kws={"color": "red"},
                    ax=ax, **kwargs)
    except Exception as e:                                   # lowess needs statsmodels
        sns.regplot(data=practice, x="hours", y="performance", order=3, scatter_kws={"alpha": 0.4},
                    line_kws={"color": "red"}, ax=ax)
        title = "order=3 (install statsmodels for lowess=True)"
    ax.set_title(title)
save_and_show(fig, "13e_regplot_fits.png")

# ---------------------------------------------------------------- 6. residplot
print("\n=== 6. residplot: patterns reveal a wrong model ===")
fig, axes = plt.subplots(1, 2, figsize=(13, 4.3))
sns.residplot(data=practice, x="hours", y="performance", ax=axes[0], scatter_kws={"alpha": 0.5})
axes[0].set_title("straight-line residuals: an arch = curve missed")
sns.residplot(data=practice, x="hours", y="performance", order=2, ax=axes[1], scatter_kws={"alpha": 0.5}, color="tab:green")
axes[1].set_title("order=2 residuals: random scatter = good")
for ax in axes:
    ax.axhline(0, color="black", lw=1)
save_and_show(fig, "13f_residplot.png")

# ---------------------------------------------------------------- 7. lmplot facets + binned estimates
print("\n=== 7. lmplot with col/hue, and x_bins for many points ===")
g = sns.lmplot(data=bills, x="total_bill", y="tip", hue="smoker", col="time", height=4.2, aspect=1.1,
               scatter_kws={"alpha": 0.5})
g.figure.suptitle("lmplot(hue='smoker', col='time')", y=1.04)
save_and_show(g.figure, "13g_lmplot_facets.png")
fig, ax = plt.subplots(figsize=(8, 5))
sns.regplot(data=bills, x="total_bill", y="tip", x_bins=8, ax=ax, color="tab:purple")
ax.set_title("x_bins=8: mean tip in 8 bill ranges + fitted line")
save_and_show(fig, "13h_regplot_xbins.png")
