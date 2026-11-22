"""Lecture 15: Seaborn styles, despine, contexts, palette families, custom palettes, colour-blind-friendly design."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import seaborn as sns  # noqa: E402
from common import get_monthly_sales, get_restaurant_bills, save_and_show  # noqa: E402

bills = get_restaurant_bills()
days = ["Thu", "Fri", "Sat", "Sun"]

# ---------------------------------------------------------------- 1. five styles
print("=== 1. The five styles ===")
styles = ["darkgrid", "whitegrid", "white", "dark", "ticks"]
fig = plt.figure(figsize=(18, 3.8))
for i, style in enumerate(styles, start=1):
    with sns.axes_style(style):
        ax = fig.add_subplot(1, 5, i)
        sns.barplot(data=bills, x="day", y="tip", order=days, errorbar=None, ax=ax)
        if style == "ticks":
            sns.despine(ax=ax, offset=6)
        ax.set_title(f"'{style}'" + (" + despine" if style == "ticks" else ""))
save_and_show(fig, "15a_styles.png")

# ---------------------------------------------------------------- 2. contexts
print("\n=== 2. Contexts scale everything for the destination ===")
sns.set_theme(style="whitegrid")
for context in ["paper", "notebook", "talk", "poster"]:
    with sns.plotting_context(context):
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.lineplot(data=get_monthly_sales(), x="Month", y="Electronics", marker="o", ax=ax)
        ax.set_title(f"context='{context}'")
        ax.set_xticks(range(0, 12, 3))
        print(f"  {context:<9} font size {plt.rcParams['font.size']:.1f}, line width {plt.rcParams['lines.linewidth']:.2f}")
        save_and_show(fig, f"15b_context_{context}.png")

# ---------------------------------------------------------------- 3. palette families
print("\n=== 3. Qualitative, sequential and diverging palettes ===")
palettes = [("deep", "qualitative"), ("colorblind", "qualitative"), ("Set2", "qualitative"),
            ("rocket", "sequential"), ("mako", "sequential"), ("light:seagreen", "sequential"),
            ("vlag", "diverging"), ("icefire", "diverging"), ("blend:#7AB,#EDA", "custom blend")]
fig, axes = plt.subplots(len(palettes), 1, figsize=(9, 7))
for ax, (name, kind) in zip(axes, palettes):
    colors = sns.color_palette(name, 8)
    ax.imshow(np.arange(8).reshape(1, -1), cmap=plt.matplotlib.colors.ListedColormap(colors), aspect="auto")
    ax.set_axis_off()
    ax.text(-0.02, 0.5, f"{name}  ({kind})", transform=ax.transAxes, ha="right", va="center", fontsize=10)
fig.subplots_adjust(left=0.33, hspace=0.4)
fig.suptitle("sns.color_palette(name, 8)", fontsize=14, fontweight="bold")
save_and_show(fig, "15c_palettes.png")

# ---------------------------------------------------------------- 4. right palette for the data
print("\n=== 4. Match the palette type to the data ===")
fig, axes = plt.subplots(1, 3, figsize=(17, 4.5))
sns.barplot(data=bills, x="day", y="total_bill", hue="day", order=days, palette="deep", errorbar=None, legend=False, ax=axes[0])
axes[0].set_title("categories -> qualitative ('deep')")
sns.scatterplot(data=bills, x="total_bill", y="tip", hue="size", palette="rocket_r", ax=axes[1])
axes[1].set_title("numeric hue -> sequential ('rocket_r')")
diff = bills.groupby("day")["tip"].mean().loc[days] - bills["tip"].mean()
sns.barplot(x=diff.index, y=diff.values, hue=diff.values, palette="vlag", legend=False, ax=axes[2])
axes[2].axhline(0, color="black", lw=0.8)
axes[2].set_title("above/below average -> diverging ('vlag')")
save_and_show(fig, "15d_palette_for_data.png")

# ---------------------------------------------------------------- 5. explicit colours + brand palette
print("\n=== 5. Exact colours per category, and a brand palette ===")
BRAND = ["#0B5394", "#E69138", "#6AA84F", "#999999"]
fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
sns.boxplot(data=bills, x="time", y="tip", hue="smoker", palette={"Yes": "#E69138", "No": "#0B5394"}, ax=axes[0])
axes[0].set_title("palette={'Yes': ..., 'No': ...}")
with sns.color_palette(BRAND):
    sns.countplot(data=bills, x="day", order=days, hue="day", legend=False, ax=axes[1])
axes[1].set_title("with sns.color_palette(BRAND): ...")
save_and_show(fig, "15e_explicit_and_brand.png")

# ---------------------------------------------------------------- 6. colour-blind-friendly
print("\n=== 6. Red/green only vs colour-blind-safe design ===")
rng = np.random.default_rng(3)
months = np.arange(12)
a = 50 + np.cumsum(rng.normal(1, 2, 12))
b = 50 + np.cumsum(rng.normal(0.3, 2, 12))
fig, (bad, good) = plt.subplots(1, 2, figsize=(14, 4.6))
bad.plot(months, a, color="#2ca02c")
bad.plot(months, b, color="#d62728")
bad.set_title("Relies on red vs green only")
good.plot(months, a, color=sns.color_palette("colorblind")[0], marker="o", lw=2.5)
good.plot(months, b, color=sns.color_palette("colorblind")[1], marker="s", ls="--", lw=2.5)
good.text(11.2, a[-1], "Plan A", color=sns.color_palette("colorblind")[0], va="center", fontweight="bold")
good.text(11.2, b[-1], "Plan B", color=sns.color_palette("colorblind")[1], va="center", fontweight="bold")
good.set_xlim(-0.3, 13)
good.set_title("Colour-blind palette + markers + dashes + direct labels")
for ax in (bad, good):
    ax.set_xlabel("Month")
save_and_show(fig, "15f_colorblind_safe.png")

# ---------------------------------------------------------------- 7. reset
sns.reset_defaults()
print("\n  sns.reset_defaults() restores Matplotlib's original look")
