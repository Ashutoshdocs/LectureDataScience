"""Lecture 02: Line plots: formatting, annotations, reference lines, bands, dates, rolling means, log scale, twin axes."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import apply_style, get_daily_visits, get_monthly_sales, save_and_show  # noqa: E402

apply_style()
df = get_monthly_sales()

# ---------------------------------------------------------------- 1. formatting (your original demo)
print("=== 1. color, linestyle, marker, linewidth + annotate the peak ===")
fig, ax = plt.subplots()
ax.plot(df["Month"], df["Electronics"], color="#1f77b4", linestyle="-", marker="o", linewidth=2, label="Electronics")
ax.plot(df["Month"], df["Clothing"], color="#ff7f0e", linestyle="--", marker="s", linewidth=2, label="Clothing")
ax.plot(df["Month"], df["Groceries"], color="#2ca02c", linestyle=":", marker="^", linewidth=2, label="Groceries")
best = df["Electronics"].idxmax()                    # row index of the maximum
ax.annotate(f"Peak: {df['Electronics'][best]}",
            xy=(best, df["Electronics"][best]),       # the point the arrow touches
            xytext=(best - 3, df["Electronics"][best] + 8),
            arrowprops=dict(arrowstyle="->", color="black"))
ax.set_title("Monthly Sales by Category")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (in thousands)")
ax.set_ylim(0, 90)
ax.legend(loc="lower right")
print(f"  Electronics peaks in {df['Month'][best]} at {df['Electronics'][best]}")
save_and_show(fig, "02a_formatting_and_annotate.png")

# ---------------------------------------------------------------- 2. line & marker gallery
print("\n=== 2. Line styles and markers at a glance ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
for i, ls in enumerate(["-", "--", ":", "-.", (0, (5, 1, 1, 1))]):
    ax1.plot([0, 10], [i, i], linestyle=ls, linewidth=2.5)
    ax1.text(10.3, i, repr(ls), va="center", family="monospace")
ax1.set_xlim(0, 14)
ax1.set_title("linestyle")
ax1.set_yticks([])
for i, m in enumerate(["o", "s", "^", "D", "x", "+", "*", "."]):
    ax2.plot(np.arange(6), np.full(6, i), marker=m, markersize=9, linestyle="none")
    ax2.text(6, i, repr(m), va="center", family="monospace")
ax2.plot(np.arange(6), np.full(6, 8.2), marker="o", markersize=9, markerfacecolor="white", linestyle="-")
ax2.text(6, 8.2, "hollow: markerfacecolor='white'", va="center", fontsize=9)
ax2.set_xlim(-0.5, 10)
ax2.set_title("marker")
ax2.set_yticks([])
save_and_show(fig, "02b_styles_gallery.png")

# ---------------------------------------------------------------- 3. reference lines, bands, direct labels
print("\n=== 3. Storytelling: target line, shaded period, min-max band, direct labels ===")
fig, ax = plt.subplots()
x = np.arange(12)
avg = df[["Electronics", "Clothing", "Groceries"]].mean(axis=1)
low = df[["Electronics", "Clothing", "Groceries"]].min(axis=1)
high = df[["Electronics", "Clothing", "Groceries"]].max(axis=1)
ax.fill_between(x, low, high, color="tab:blue", alpha=0.15, label="min-max range")
ax.plot(x, avg, color="tab:blue", lw=2.5, label="average of categories")
ax.axhline(50, color="red", ls="--", lw=1)
ax.text(11.2, 50.8, "target 50", color="red", ha="right")
ax.axvspan(5.5, 7.5, color="gold", alpha=0.25)
ax.text(6.5, 72, "summer\nsale", ha="center")
for col, color in [("Electronics", "tab:green"), ("Groceries", "tab:gray")]:
    ax.plot(x, df[col], color=color, lw=1.2)
    ax.text(11.15, df[col].iloc[-1], col, color=color, va="center")       # label at the line end
ax.set_xticks(x, df["Month"])
ax.set_xlim(-0.3, 13.2)
ax.set_title("Average sales vs target, with the category range")
ax.set_ylabel("Sales (in thousands)")
ax.legend(loc="upper left")
save_and_show(fig, "02c_storytelling.png")

# ---------------------------------------------------------------- 4. dates + rolling mean
print("\n=== 4. Daily time series: date ticks and a 7-day rolling average ===")
visits = get_daily_visits()
visits["rolling_7"] = visits["visits"].rolling(7, center=True).mean()
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(visits["date"], visits["visits"], color="lightgray", lw=1, label="daily")
ax.plot(visits["date"], visits["rolling_7"], color="tab:blue", lw=2.5, label="7-day average")
spike = visits.loc[visits["visits"].idxmax()]
ax.axvspan(visits["date"][100], visits["date"][106], color="tab:orange", alpha=0.2, label="campaign")
ax.annotate(f"campaign peak\n{spike['visits']:,} visits", xy=(spike["date"], spike["visits"]),
            xytext=(visits["date"][40], spike["visits"] - 200), arrowprops=dict(arrowstyle="->"))
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax.set_title("Website visits: noisy daily values vs the smoothed trend")
ax.set_ylabel("Visits per day")
ax.legend(loc="upper left")
print(f"  {len(visits)} days; weekday mean {visits.loc[visits['date'].dt.dayofweek < 5, 'visits'].mean():.0f}, "
      f"weekend mean {visits.loc[visits['date'].dt.dayofweek >= 5, 'visits'].mean():.0f}")
save_and_show(fig, "02d_dates_rolling.png")

# ---------------------------------------------------------------- 5. log scale
print("\n=== 5. Linear vs log scale ===")
n = np.arange(1, 21)
fig, (lin, log) = plt.subplots(1, 2, figsize=(12, 4.5))
for ax, scale in [(lin, "linear"), (log, "log")]:
    ax.plot(n, n, marker=".", label="n")
    ax.plot(n, n ** 2, marker=".", label="n²")
    ax.plot(n, 2.0 ** n, marker=".", label="2ⁿ")
    ax.set_yscale(scale)
    ax.set_title(f"y-scale = '{scale}'")
    ax.set_xlabel("n")
    ax.legend()
print("  on the log scale, exponential growth (2^n) becomes a straight line")
save_and_show(fig, "02e_log_scale.png")

# ---------------------------------------------------------------- 6. twin axes
print("\n=== 6. twinx(): two units on one chart (use with care) ===")
weekly = visits.set_index("date")[["visits", "signups"]].resample("W").sum()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(weekly.index, weekly["visits"], color="tab:blue", marker="o", label="visits")
ax.set_ylabel("Weekly visits", color="tab:blue")
ax.tick_params(axis="y", labelcolor="tab:blue")
ax2 = ax.twinx()                                    # shares x, has its own y-axis
ax2.plot(weekly.index, weekly["signups"], color="tab:red", marker="s", label="signups")
ax2.set_ylabel("Weekly signups", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax2.grid(False)
ax.set_title("Visits and signups (each axis coloured like its line)")
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
save_and_show(fig, "02f_twin_axes.png")

# ---------------------------------------------------------------- 7. step plot
print("\n=== 7. Step line for values that stay constant until they change ===")
fig, ax = plt.subplots(figsize=(9, 4))
price_days = [0, 10, 25, 40, 60, 90]
prices = [499, 449, 449, 399, 429, 379]
ax.plot(price_days, prices, drawstyle="steps-post", lw=2, marker="o")
ax.set_title("Product price over time (steps-post)")
ax.set_xlabel("Day")
ax.set_ylabel("Price (Rs)")
save_and_show(fig, "02g_step.png")
