"""Lecture 19: Checker for the visualization exercises.

    python lecture.py             -> checks solutions.py (should be 15/15) and saves every solution chart
    python lecture.py exercises   -> checks YOUR exercises.py and saves your charts to output/

The checker inspects the returned Figure objects: lines, bars, text, titles, labels, scales, spines.
"""
import importlib
import os
import pathlib
import sys

os.environ.setdefault("MPLBACKEND", "Agg")
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import matplotlib  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.container import BarContainer  # noqa: E402
from matplotlib.patches import Wedge  # noqa: E402
from common import get_market_share, get_monthly_sales, get_students, output_dir  # noqa: E402

target = sys.argv[1] if len(sys.argv) > 1 else "solutions"
m = importlib.import_module(target)
sales, students, share = get_monthly_sales(), get_students(), get_market_share()
CATS = ["Electronics", "Clothing", "Groceries"]


def need(cond, message):
    if not cond:
        raise AssertionError(message)


def get_fig(result):
    need(isinstance(result, matplotlib.figure.Figure), f"must return a Figure, got {type(result).__name__}")
    return result


def bars_of(ax):
    return [c for c in ax.containers if isinstance(c, BarContainer)]


def check_01():
    fig = get_fig(m.ex01_line(sales))
    ax = fig.axes[0]
    need(len(ax.get_lines()) >= 1, "no line drawn")
    line = ax.get_lines()[0]
    need(np.allclose(line.get_ydata(), sales["Electronics"]), "line y-values are not Electronics")
    need(line.get_marker() == "o", f"marker is {line.get_marker()!r}, expected 'o'")
    need(ax.get_title() == "Electronics", f"title is {ax.get_title()!r}")
    need((ax.get_xlabel(), ax.get_ylabel()) == ("Month", "Sales"), "axis labels must be 'Month' and 'Sales'")
    return fig


def check_02():
    fig = get_fig(m.ex02_three_lines_legend(sales))
    ax = fig.axes[0]
    labels = [ln.get_label() for ln in ax.get_lines()]
    need(labels[:3] == CATS, f"line labels {labels} should be {CATS}")
    need(ax.get_legend() is not None, "no legend")
    return fig


def check_03():
    fig = get_fig(m.ex03_annotate_peak(sales))
    ax = fig.axes[0]
    anns = [t for t in ax.texts if isinstance(t, matplotlib.text.Annotation)]
    need(anns, "no ax.annotate found")
    ann = anns[0]
    need(ann.get_text() == "Peak", f"annotation text is {ann.get_text()!r}")
    i = int(sales["Electronics"].idxmax())
    need(np.allclose(ann.xy, (i, sales["Electronics"][i])), f"annotation points at {ann.xy}, expected {(i, sales['Electronics'][i])}")
    return fig


def check_04():
    totals = sales[CATS].sum()
    fig = get_fig(m.ex04_sorted_barh(totals))
    ax = fig.axes[0]
    conts = bars_of(ax)
    need(conts and conts[0].orientation == "horizontal", "use ax.barh")
    widths = [p.get_width() for p in conts[0]]
    ys = [p.get_y() for p in conts[0]]
    top_bar_width = widths[int(np.argmax(ys))]
    need(np.isclose(top_bar_width, totals.max()), "the largest bar must be at the top")
    need(len(ax.texts) >= 3, "add value labels with ax.bar_label")
    return fig


def check_05():
    fig = get_fig(m.ex05_grouped_bars(sales))
    ax = fig.axes[0]
    conts = bars_of(ax)
    need(len(conts) == 3, f"expected 3 bar containers, got {len(conts)}")
    need(all(len(c) == 6 for c in conts), "each series needs 6 bars (Jan-Jun)")
    need(np.isclose(conts[0][0].get_width(), 0.27), "bar width must be 0.27")
    need([t.get_text() for t in ax.get_xticklabels()][:6] == list(sales["Month"][:6]), "x tick labels must be the month names")
    need(ax.get_legend() is not None, "no legend")
    return fig


def check_06():
    fig = get_fig(m.ex06_stacked_bars(sales))
    ax = fig.axes[0]
    conts = bars_of(ax)
    need(len(conts) == 3, f"expected 3 stacked series, got {len(conts)}")
    tops = [max(c[i].get_y() + c[i].get_height() for c in conts) for i in range(6)]
    need(np.allclose(tops, sales[CATS].head(6).sum(axis=1)), "stack tops must equal the monthly totals (use bottom=)")
    need(np.allclose([p.get_y() for p in conts[0]], 0), "Electronics must be at the bottom")
    return fig


def check_07():
    fig = get_fig(m.ex07_donut(share))
    ax = fig.axes[0]
    wedges = [p for p in ax.patches if isinstance(p, Wedge)]
    need(len(wedges) == len(share), f"expected {len(share)} wedges, got {len(wedges)}")
    need(all(w.width is not None and np.isclose(w.width, 0.4) for w in wedges), "use wedgeprops={'width': 0.4}")
    need(any(t.get_text() == "Total" for t in ax.texts), "add the text 'Total' in the centre")
    return fig


def check_08():
    fig = get_fig(m.ex08_hist_mean(students["score"]))
    ax = fig.axes[0]
    need(len(ax.patches) == 10, f"expected 10 bins (range(0, 101, 10)), got {len(ax.patches)}")
    vlines = [ln for ln in ax.get_lines() if np.allclose(ln.get_xdata(), students["score"].mean())]
    need(vlines, "no vertical line at the mean (ax.axvline)")
    need(vlines[0].get_linestyle() == "--", "the mean line must be dashed")
    need(matplotlib.colors.same_color(vlines[0].get_color(), "red"), "the mean line must be red")
    return fig


def check_09():
    fig = get_fig(m.ex09_scatter_trend(students))
    ax = fig.axes[0]
    need(ax.collections, "no scatter points")
    need(len(ax.get_lines()) >= 1, "no trend line")
    r = students["study_hours"].corr(students["score"])
    need(f"r = {r:.2f}" in ax.get_title(), f"title must contain 'r = {r:.2f}'")
    return fig


def check_10():
    fig = get_fig(m.ex10_subplots_shared(sales))
    axes = fig.axes
    need(len(axes) == 3, f"expected 3 axes, got {len(axes)}")
    need([a.get_title() for a in axes] == CATS, "titles must be the category names in order")
    need(axes[0].get_shared_y_axes().joined(axes[0], axes[2]), "use sharey=True")
    return fig


def check_11():
    fig = get_fig(m.ex11_log_scale())
    ax = fig.axes[0]
    need(ax.get_yscale() == "log", f"y-scale is {ax.get_yscale()!r}, expected 'log'")
    need(np.isclose(max(ax.get_lines()[0].get_ydata()), 2 ** 20), "plot 2**n up to n = 20")
    return fig


def check_12():
    fig = get_fig(m.ex12_sns_box(students))
    ax = fig.axes[0]
    labels = [t.get_text() for t in ax.get_xticklabels()]
    need(labels == ["Freshman", "Sophomore", "Junior", "Senior"], f"category order is {labels}")
    need(len(ax.patches) >= 4 or len(ax.get_lines()) >= 4, "no boxes drawn")
    return fig


def check_13():
    fig = get_fig(m.ex13_sns_heatmap(students))
    ax = fig.axes[0]
    need(ax.collections, "no heatmap drawn")
    mesh = ax.collections[0]
    need(np.isclose(mesh.norm.vmin, -1) and np.isclose(mesh.norm.vmax, 1), "set vmin=-1, vmax=1")
    need(sum(t.get_text() == "1" or t.get_text() == "1.00" for t in ax.texts) >= 3, "use annot=True")
    return fig


def check_14():
    fig = get_fig(m.ex14_sns_hue_scatter(students))
    ax = fig.axes[0]
    leg = ax.get_legend()
    need(leg is not None, "no legend: did you pass hue='gender'?")
    texts = {t.get_text() for t in leg.get_texts()}
    need({"Male", "Female"} <= texts, f"legend shows {texts}")
    return fig


def check_15():
    fig = get_fig(m.ex15_declutter(sales))
    ax = fig.axes[0]
    need(not ax.spines["top"].get_visible() and not ax.spines["right"].get_visible(), "hide the top and right spines")
    need(ax.get_title(loc="left") != "", "use ax.set_title(..., loc='left')")
    need(np.isclose(ax.get_ylim()[0], 0), f"y-axis must start at 0 (it starts at {ax.get_ylim()[0]:.1f})")
    return fig


TITLES = ["line + labels", "3 lines + legend", "annotate peak", "sorted barh", "grouped bars", "stacked bars",
          "donut", "histogram + mean", "scatter + trend", "shared subplots", "log scale", "sns boxplot",
          "sns heatmap", "sns hue scatter", "declutter"]
CHECKS = [globals()[f"check_{i:02d}"] for i in range(1, 16)]

print(f"Checking {target}.py\n")
score = 0
out = output_dir()
for num, (title, check) in enumerate(zip(TITLES, CHECKS), start=1):
    try:
        fig = check()
    except Exception as e:
        kind = "" if isinstance(e, AssertionError) else type(e).__name__ + ": "
        print(f"  ✘ {num:02d} {title:<18} {kind}{str(e).splitlines()[0][:100] if str(e) else ''}")
    else:
        score += 1
        fig.savefig(out / f"{target}_{num:02d}.png", dpi=80, bbox_inches="tight")
        print(f"  ✔ {num:02d} {title}")
    plt.close("all")
print(f"\n  Score: {score} / {len(CHECKS)}   (passing charts saved to output/{target}_NN.png)")

if target == "solutions" and score != len(CHECKS):
    sys.exit(1)
