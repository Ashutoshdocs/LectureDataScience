"""Lecture 17: Project: a one-page sales dashboard with Matplotlib (KPI tiles + 6 charts via subplot_mosaic)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.ticker import FuncFormatter  # noqa: E402
from common import (CATEGORIES, apply_style, get_daily_visits, get_market_share, get_monthly_sales,  # noqa: E402
                    get_regional_sales, save_and_show)

apply_style()
BRAND = {"Electronics": "#0B5394", "Clothing": "#E69138", "Groceries": "#6AA84F", "muted": "#B7B7B7",
         "good": "#2E7D32", "bad": "#C62828"}

# ---------------------------------------------------------------- 1. data & KPIs
sales = get_monthly_sales()
visits = get_daily_visits()
regional = get_regional_sales()
share = get_market_share()

sales["Total"] = sales[CATEGORIES].sum(axis=1)
h1, h2 = sales["Total"][:6].sum(), sales["Total"][6:].sum()
kpis = {
    "Total sales": (f"Rs {sales['Total'].sum():,.0f}k", f"H2 vs H1: {h2 / h1 - 1:+.1%}", h2 >= h1),
    "Best month": (sales.loc[sales["Total"].idxmax(), "Month"], f"Rs {sales['Total'].max():.0f}k", True),
    "Avg daily visits": (f"{visits['visits'].mean():,.0f}", f"last 30d: {visits['visits'][-30:].mean() / visits['visits'][:30].mean() - 1:+.0%} vs first 30d", True),
    "Conversion rate": (f"{visits['signups'].sum() / visits['visits'].sum():.2%}", f"{visits['signups'].sum():,} signups", True),
}
region_total = regional.groupby("region")[["sales", "target"]].sum()
region_total["vs_target"] = region_total["sales"] / region_total["target"] - 1
print("=== KPIs ===")
for name, (value, sub, good) in kpis.items():
    print(f"  {name:<17} {value:>12}   {sub}")
print("\n=== Regions vs target ===")
print(region_total.round(3).to_string())

# ---------------------------------------------------------------- 2. layout
layout = [["k1", "k2", "k3", "k4"],
          ["trend", "trend", "trend", "share"],
          ["region", "region", "mix", "mix"],
          ["visits", "visits", "visits", "weekday"]]
fig, ax = plt.subplot_mosaic(layout, figsize=(18, 17), layout="constrained",
                             gridspec_kw={"height_ratios": [0.55, 1.4, 1.2, 1.2]})
fig.suptitle("Sales & Traffic Dashboard: 2026", fontsize=22, fontweight="bold", x=0.02, ha="left")
fig.text(0.99, -0.01, "Generated with Matplotlib | data: common.py sample data", fontsize=10, color="gray", ha="right")

# ---------------------------------------------------------------- 3. KPI tiles
for key, (name, (value, sub, good)) in zip(["k1", "k2", "k3", "k4"], kpis.items()):
    a = ax[key]
    a.set_axis_off()
    a.add_patch(plt.Rectangle((0, 0), 1, 1, transform=a.transAxes, facecolor="#F3F6FA", edgecolor="#D0D7E2", lw=1.5))
    a.text(0.06, 0.72, name.upper(), transform=a.transAxes, fontsize=11, color="#5B6678", fontweight="bold")
    a.text(0.06, 0.36, value, transform=a.transAxes, fontsize=24, fontweight="bold", color="#18202E")
    a.text(0.06, 0.1, sub, transform=a.transAxes, fontsize=10, color=BRAND["good"] if good else BRAND["bad"])

# ---------------------------------------------------------------- 4. monthly trend (stacked area + total line)
a = ax["trend"]
x = np.arange(12)
a.stackplot(x, [sales[c] for c in CATEGORIES], colors=[BRAND[c] for c in CATEGORIES], alpha=0.85, labels=CATEGORIES)
a.plot(x, sales["Total"], color="black", lw=2, marker="o", label="Total")
best = sales["Total"].idxmax()
a.annotate(f"best month\nRs {sales['Total'][best]:.0f}k", xy=(best, sales["Total"][best]), xytext=(best - 3, sales["Total"][best] + 18),
           arrowprops=dict(arrowstyle="->"), fontsize=10)
a.set_xticks(x, sales["Month"])
a.set_ylim(0, sales["Total"].max() * 1.3)
a.set_title("Monthly sales by category", loc="left")
a.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0f}k"))
a.legend(loc="upper left", ncols=4, frameon=False)

# ---------------------------------------------------------------- 5. market share donut
a = ax["share"]
colors = [BRAND["Electronics"]] + [BRAND["muted"]] * (len(share) - 1)
a.pie(share.values(), labels=share.keys(), colors=colors, startangle=90, counterclock=False, autopct="%1.0f%%",
      pctdistance=0.78, wedgeprops={"width": 0.38, "edgecolor": "white"}, textprops={"fontsize": 9})
a.text(0, 0, "Brand A\nleads", ha="center", va="center", fontsize=12, fontweight="bold")
a.set_title("Market share", loc="left")

# ---------------------------------------------------------------- 6. regions vs target
a = ax["region"]
rt = region_total.sort_values("sales")
bars = a.barh(rt.index, rt["sales"], color=[BRAND["good"] if v >= 0 else BRAND["bad"] for v in rt["vs_target"]], alpha=0.85)
a.scatter(rt["target"], rt.index, marker="|", s=900, color="black", zorder=3, label="target")
a.bar_label(bars, labels=[f"{s:,.0f}  ({v:+.0%})" for s, v in zip(rt["sales"], rt["vs_target"])], padding=4, fontsize=10)
a.set_xlim(0, rt["sales"].max() * 1.3)
a.set_title("Annual sales by region vs target (green = above target)", loc="left")
a.set_xlabel("Sales (lakh)")
a.legend(loc="lower right")

# ---------------------------------------------------------------- 7. product mix heatmap
a = ax["mix"]
mix = regional.pivot_table(index="region", columns="product", values="sales", aggfunc="sum")
im = a.imshow(mix.values, cmap="Blues", aspect="auto")
a.set_xticks(range(mix.shape[1]), mix.columns)
a.set_yticks(range(mix.shape[0]), mix.index)
a.grid(False)
for i in range(mix.shape[0]):
    for j in range(mix.shape[1]):
        v = mix.values[i, j]
        a.text(j, i, f"{v:.0f}", ha="center", va="center", color="white" if v > mix.values.mean() else "black", fontsize=11)
fig.colorbar(im, ax=a, label="lakh", shrink=0.8)
a.set_title("Product mix by region", loc="left")

# ---------------------------------------------------------------- 8. daily visits with rolling mean + campaign
a = ax["visits"]
a.plot(visits["date"], visits["visits"], color=BRAND["muted"], lw=0.8, label="daily")
a.plot(visits["date"], visits["visits"].rolling(7, center=True).mean(), color=BRAND["Electronics"], lw=2.5, label="7-day average")
a.axvspan(visits["date"][100], visits["date"][106], color=BRAND["Clothing"], alpha=0.2, label="campaign")
a.xaxis.set_major_locator(mdates.MonthLocator())
a.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
a.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:.1f}k"))
a.set_title("Website visits per day", loc="left")
a.legend(loc="upper left", ncols=3, frameon=False)

# ---------------------------------------------------------------- 9. weekday pattern
a = ax["weekday"]
order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
by_day = visits.assign(day=visits["date"].dt.day_name().str[:3]).groupby("day")["visits"].mean().loc[order]
wb = a.bar(order, by_day, color=[BRAND["Electronics"] if d not in ("Sat", "Sun") else BRAND["muted"] for d in order])
a.bar_label(wb, labels=[f"{v / 1000:.1f}k" for v in by_day], fontsize=9, padding=2)
a.set_title("Avg visits by weekday", loc="left")
a.set_ylim(0, by_day.max() * 1.2)
a.grid(False)

for key in ["trend", "region", "visits", "weekday"]:
    ax[key].spines[["top", "right"]].set_visible(False)

print("\n=== Insights printed for the report ===")
print(f"  1. Sales rose {h2 / h1 - 1:+.1%} from H1 to H2; Electronics drives the growth.")
print(f"  2. Below target for the year: {', '.join(region_total.index[region_total['vs_target'] < 0])}.")
print(f"  3. Weekends get {1 - by_day[['Sat', 'Sun']].mean() / by_day[order[:5]].mean():.0%} fewer visits than weekdays.")
campaign = visits.iloc[100:107]
lift = campaign["visits"].mean() / visits["visits"].iloc[86:100].mean()
print(f"  4. The {campaign['date'].iloc[0]:%B} campaign ({campaign['date'].iloc[0]:%d %b}-{campaign['date'].iloc[-1]:%d %b}) lifted daily visits {lift:.1f}x for a week.")
save_and_show(fig, "17_sales_dashboard.png", dpi=110)
