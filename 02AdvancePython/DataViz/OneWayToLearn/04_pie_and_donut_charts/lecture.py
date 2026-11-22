"""Lecture 04: Pie and donut charts: explode, autopct functions, donuts with a centre total, nested donuts,
and why bars are often better."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import apply_style, get_market_share, save_and_show  # noqa: E402

apply_style()
share = get_market_share()
labels = list(share.keys())
sizes = list(share.values())

# ---------------------------------------------------------------- 1. classic pie + donut (your original demo)
print("=== 1. Classic pie with an exploded slice, and a donut ===")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
ax1.pie(sizes, labels=labels, autopct="%1.1f%%", explode=[0.1, 0, 0, 0, 0], startangle=90,
        counterclock=False, shadow=True, wedgeprops={"edgecolor": "white"})
ax1.set_title("Smartphone Market Share")
ax1.axis("equal")
ax2.pie(sizes, labels=labels, autopct="%1.0f%%", startangle=90, counterclock=False, pctdistance=0.8,
        wedgeprops={"width": 0.4, "edgecolor": "white"})
ax2.text(0, 0, "2026", ha="center", va="center", fontsize=16, fontweight="bold")
ax2.set_title("Donut Chart Version")
save_and_show(fig, "04a_pie_and_donut.png")

# ---------------------------------------------------------------- 2. autopct as a function, one highlighted slice
print("\n=== 2. Value + percentage labels; highlight one slice, mute the rest ===")
market_size = 4.2                                                  # crore units
colors = ["tab:blue"] + ["#d0d7e2"] * 4


def label_with_value(pct):
    return f"{pct:.0f}%\n({pct * market_size / 100:.2f} Cr)"


fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct=label_with_value, startangle=90, counterclock=False,
                                  colors=colors, wedgeprops={"edgecolor": "white", "linewidth": 2})
autotexts[0].set_color("white")
autotexts[0].set_fontweight("bold")
ax.set_title("Brand A sells a third of all smartphones")
print("  pie() returns", len(wedges), "wedges,", len(texts), "labels and", len(autotexts), "percentage texts")
save_and_show(fig, "04b_pie_highlight.png")

# ---------------------------------------------------------------- 3. donut with a headline total
print("\n=== 3. Donut with the total in the centre ===")
fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.pie(sizes, labels=labels, autopct="%1.0f%%", pctdistance=0.8, startangle=90, counterclock=False,
       wedgeprops={"width": 0.38, "edgecolor": "white", "linewidth": 2}, textprops={"fontsize": 11})
ax.text(0, 0.08, f"{market_size} Cr", ha="center", va="center", fontsize=24, fontweight="bold")
ax.text(0, -0.15, "phones sold", ha="center", va="center", fontsize=11, color="gray")
ax.set_title("Market share, 2026")
save_and_show(fig, "04c_donut_total.png")

# ---------------------------------------------------------------- 4. nested donut
print("\n=== 4. Nested donut: brands (inner) split into online/offline (outer) ===")
online_share = [0.6, 0.45, 0.7, 0.3, 0.5]
outer = np.array([[s * o, s * (1 - o)] for s, o in zip(sizes, online_share)]).ravel()
cmap = plt.colormaps["tab20c"]
inner_colors = cmap(np.arange(5) * 4)
outer_colors = cmap(np.array([[i * 4 + 1, i * 4 + 2] for i in range(5)]).ravel())
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(sizes, radius=0.7, labels=labels, labeldistance=0.55, colors=inner_colors,
       wedgeprops={"width": 0.3, "edgecolor": "white"}, startangle=90, counterclock=False, textprops={"fontsize": 9})
ax.pie(outer, radius=1.0, colors=outer_colors, wedgeprops={"width": 0.3, "edgecolor": "white"},
       startangle=90, counterclock=False, autopct=lambda p: f"{p:.0f}%" if p > 4 else "", pctdistance=0.85,
       textprops={"fontsize": 8})
ax.set_title("Inner: brand share | Outer: online (darker) vs offline")
save_and_show(fig, "04d_nested_donut.png")

# ---------------------------------------------------------------- 5. why bars are often better
print("\n=== 5. Similar slices: pie vs bar ===")
close = {"North": 24, "South": 26, "East": 25, "West": 25}
fig, (p, b) = plt.subplots(1, 2, figsize=(12, 4.8))
p.pie(close.values(), labels=close.keys(), startangle=90, counterclock=False, wedgeprops={"edgecolor": "white"})
p.set_title("Which region is biggest? (pie)")
ordered = dict(sorted(close.items(), key=lambda kv: kv[1]))
hb = b.barh(list(ordered.keys()), list(ordered.values()), color="tab:blue")
b.bar_label(hb, fmt="%d%%", padding=3)
b.set_xlim(0, 30)
b.set_title("Which region is biggest? (sorted bars)")
print("  The pie hides that South (26%) leads and North (24%) trails; the bars make it obvious.")
save_and_show(fig, "04e_pie_vs_bar.png")
