"""Lecture 09: Colours, colormaps, tick formatters, spines, text/annotations, legends, styles, rcParams,
and a before/after declutter."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.ticker import FuncFormatter, MultipleLocator, PercentFormatter, StrMethodFormatter  # noqa: E402
from common import CATEGORIES, apply_style, get_monthly_sales, save_and_show  # noqa: E402

apply_style()
df = get_monthly_sales()
x = np.arange(12)

# ---------------------------------------------------------------- 1. colour specifications
print("=== 1. Ways to specify a colour ===")
specs = ["steelblue", "C1", "tab:green", "#d62728", (0.58, 0.40, 0.74), "0.5"]
fig, ax = plt.subplots(figsize=(10, 3))
for i, c in enumerate(specs):
    ax.bar(i, 1, color=c)
    ax.text(i, 1.05, repr(c), ha="center", family="monospace", fontsize=9)
ax.set_xlim(-0.6, len(specs) - 0.4)
ax.set_ylim(0, 1.3)
ax.axis("off")
ax.set_title("color= accepts names, cycle codes, hex, RGB tuples and grey levels")
save_and_show(fig, "09a_colour_specs.png")

# ---------------------------------------------------------------- 2. colormaps
print("\n=== 2. Colormap families (and why to avoid jet) ===")
gradient = np.linspace(0, 1, 256).reshape(1, -1)
cmaps = [("viridis", "sequential (default)"), ("Blues", "sequential"), ("coolwarm", "diverging"),
         ("RdBu", "diverging"), ("tab10", "qualitative"), ("jet", "AVOID: fake bands")]
fig, axes = plt.subplots(len(cmaps), 1, figsize=(9, 4.5))
for ax, (name, kind) in zip(axes, cmaps):
    ax.imshow(gradient, aspect="auto", cmap=name)
    ax.set_axis_off()
    ax.text(-0.01, 0.5, f"{name}  ({kind})", transform=ax.transAxes, ha="right", va="center", fontsize=10)
fig.suptitle("Colormaps", fontsize=14, fontweight="bold")
fig.subplots_adjust(left=0.32)
save_and_show(fig, "09b_colormaps.png")
print("  5 colours sampled from viridis (RGB):", np.round(plt.colormaps["viridis"](np.linspace(0, 1, 5))[:, :3], 2).tolist())

# ---------------------------------------------------------------- 3. tick formatters and locators
print("\n=== 3. Number formatting on axes ===")
revenue = df["Electronics"] * 1000 * 85            # pretend rupees
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
axes[0].plot(x, revenue, marker="o")
axes[0].set_title("default: 6000000?")
axes[1].plot(x, revenue, marker="o")
axes[1].yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"Rs {v / 1e5:.0f}L"))
axes[1].set_title("FuncFormatter: Rs lakh")
share = df["Electronics"] / df[CATEGORIES].sum(axis=1)
axes[2].plot(x, share, marker="o", color="tab:green")
axes[2].yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals=0))
axes[2].yaxis.set_major_locator(MultipleLocator(0.05))
axes[2].set_title("PercentFormatter + MultipleLocator(5%)")
for ax in axes:
    ax.set_xticks(x[::2], df["Month"][::2])
save_and_show(fig, "09c_tick_formatters.png")
fig, ax = plt.subplots(figsize=(7, 3))
ax.barh(CATEGORIES, df[CATEGORIES].sum() * 1000, color="tab:purple")
ax.xaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
ax.set_title("StrMethodFormatter('{x:,.0f}'): thousands separators")
save_and_show(fig, "09d_strmethod.png")

# ---------------------------------------------------------------- 4. text, transforms, mathtext, legends outside
print("\n=== 4. Text in data vs axes coordinates, boxes, mathtext, legend outside ===")
fig, ax = plt.subplots()
for cat in CATEGORIES:
    ax.plot(x, df[cat], marker="o", label=cat)
ax.text(0.02, 0.95, "transform=ax.transAxes\n(always top-left)", transform=ax.transAxes, va="top",
        bbox=dict(boxstyle="round", fc="lightyellow", ec="gray"))
ax.text(9, 66, "data coords (9, 66)", ha="center", color="tab:blue")
mu = df["Electronics"].mean()
ax.axhline(mu, color="tab:blue", ls=":", lw=1)
ax.text(11, mu + 1, rf"$\mu = {mu:.1f}$", ha="right", color="tab:blue", fontsize=12)
ax.set_xticks(x, df["Month"])
ax.set_title("Text placement and a legend outside the axes", loc="left")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncols=3, frameon=False)
save_and_show(fig, "09e_text_and_legends.png")

# ---------------------------------------------------------------- 5. styles
print("\n=== 5. Built-in styles (plt.style.context) ===")
print("  available:", len(plt.style.available), "styles, e.g.", plt.style.available[:5])
styles = ["default", "ggplot", "fivethirtyeight", "dark_background", "bmh", "seaborn-v0_8-whitegrid"]
fig = plt.figure(figsize=(15, 8))
for i, style in enumerate(styles, start=1):
    with plt.style.context(style):
        ax = fig.add_subplot(2, 3, i)
        for cat in CATEGORIES:
            ax.plot(x, df[cat])
        ax.set_title(style, fontsize=11)
        ax.set_xticks([])
save_and_show(fig, "09f_styles.png")
apply_style()

# ---------------------------------------------------------------- 6. diverging colours for +/- values
print("\n=== 6. Diverging colours: profit and loss ===")
profit = (df["Electronics"] - df["Electronics"].mean()).round(1)
colors = np.where(profit >= 0, "seagreen", "indianred")
fig, ax = plt.subplots()
bars = ax.bar(df["Month"], profit, color=colors)
ax.bar_label(bars, fmt="%+.1f", padding=2, fontsize=9)
ax.axhline(0, color="black", lw=0.8)
ax.set_title("Electronics vs its yearly average (green = above, red = below)")
ax.set_ylabel("Difference (thousands)")
save_and_show(fig, "09g_diverging_bars.png")

# ---------------------------------------------------------------- 7. before / after declutter
print("\n=== 7. Declutter: default vs storytelling version ===")
fig, (before, after) = plt.subplots(1, 2, figsize=(15, 5.5))
for cat in CATEGORIES:
    before.plot(df["Month"], df[cat], marker="o", label=cat)
before.legend()
before.set_title("Before: default chart")
before.grid(True)

for cat in CATEGORIES:
    color = "tab:blue" if cat == "Electronics" else "0.7"
    lw = 3 if cat == "Electronics" else 1.5
    after.plot(x, df[cat], color=color, lw=lw)
    after.text(11.3, df[cat].iloc[-1], cat, color=color, va="center", fontweight="bold" if color != "0.7" else "normal")
growth = (df["Electronics"].iloc[-1] / df["Electronics"].iloc[0] - 1)
after.annotate(f"+{growth:.0%} since January", xy=(11, df["Electronics"].iloc[-1]), xytext=(6.5, 76),
               arrowprops=dict(arrowstyle="->", color="tab:blue"), color="tab:blue", fontsize=11)
after.spines[["top", "right"]].set_visible(False)
after.grid(axis="x", visible=False)
after.grid(axis="y", alpha=0.4)
after.set_xticks(x, df["Month"])
after.set_xlim(-0.3, 13.5)
after.set_ylim(20, 85)
after.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"Rs {v:.0f}k"))
after.set_title("After: Electronics is pulling away from other categories", loc="left")
print(f"  insight in the title; Electronics grew {growth:.0%}")
save_and_show(fig, "09h_declutter_before_after.png")

# ---------------------------------------------------------------- 8. rcParams
print("\n=== 8. rcParams: change defaults for every chart ===")
print("  current font.size:", plt.rcParams["font.size"], "| figure.figsize:", plt.rcParams["figure.figsize"])
with plt.rc_context({"font.size": 14, "axes.spines.top": False, "axes.spines.right": False, "lines.linewidth": 3}):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x, df["Electronics"])
    ax.set_title("rc_context: bigger font, no top/right spines, thick lines")
    save_and_show(fig, "09i_rc_context.png")
