"""Lecture 01: Figure / Axes / Axis / Artist, pyplot vs object-oriented, figsize, dpi, formats."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import apply_style, output_dir, save_and_show  # noqa: E402

apply_style()
x = np.linspace(0, 10, 100)                      # 100 evenly spaced points from 0 to 10

# ---------------------------------------------------------------- 1. pyplot interface
print("=== 1. pyplot (state-based): acts on the 'current' figure ===")
plt.figure()                                     # new current figure
plt.plot(x, np.sin(x), label="sin(x)")
plt.plot(x, np.cos(x), label="cos(x)", linestyle="--")
plt.title("pyplot interface: sin and cos")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
print("  current figure:", plt.gcf(), "| current axes:", type(plt.gca()).__name__)
save_and_show(plt.gcf(), "01a_pyplot_interface.png")

# ---------------------------------------------------------------- 2. OO interface
print("\n=== 2. Object-oriented: explicit fig and ax (recommended) ===")
fig, ax = plt.subplots()
line_sin, = ax.plot(x, np.sin(x), label="sin(x)")         # plot returns a LIST of Line2D artists
line_cos, = ax.plot(x, np.cos(x), label="cos(x)", linestyle="--")
ax.set_title("Object-oriented interface: sin and cos")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()
line_cos.set_color("tab:red")                    # artists can be changed after drawing
print("  type(fig)      :", type(fig).__name__)
print("  type(ax)       :", type(ax).__name__)
print("  type(ax.xaxis) :", type(ax.xaxis).__name__)
print("  artists on ax  :", [type(a).__name__ for a in ax.get_lines()], "+ title text:", repr(ax.get_title()))
save_and_show(fig, "01b_oo_interface.png")

# ---------------------------------------------------------------- 3. labelled anatomy
print("\n=== 3. The anatomy of a figure, labelled ===")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, 2 + np.sin(x), marker="o", markevery=10, label="a Line2D with markers")
ax.bar([2, 4, 6, 8], [0.6, 1.0, 0.8, 1.2], width=0.6, alpha=0.5, label="bars (Rectangles)")
ax.set_title("Axes title (ax.set_title)")
ax.set_xlabel("x-axis label (ax.set_xlabel)")
ax.set_ylabel("y-axis label (ax.set_ylabel)")
ax.legend(loc="upper right", title="Legend (ax.legend)")
fig.suptitle("Figure title (fig.suptitle)", fontsize=16, fontweight="bold")
notes = [((0.3, 3.1), "Axes = the plot area"), ((5.0, 0.15), "major ticks + tick labels"),
         ((7.5, 2.9), "Artist: a Line2D")]
for (nx, ny), text in notes:
    ax.annotate(text, xy=(nx, ny), fontsize=10, color="darkred",
                bbox=dict(boxstyle="round", fc="lightyellow", ec="darkred"))
ax.set_ylim(0, 3.6)
fig.patch.set_edgecolor("gray")
fig.patch.set_linewidth(3)                       # draw a border so you can see the Figure's edge
save_and_show(fig, "01c_anatomy_labelled.png")

# ---------------------------------------------------------------- 4. size, dpi and formats
print("\n=== 4. figsize, dpi and file formats ===")
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.plot(x, np.sin(x))
ax.set_title("Same figure, different exports")
out = output_dir()
for name, kwargs in [("01d_low_dpi.png", {"dpi": 72}), ("01d_high_dpi.png", {"dpi": 300}),
                     ("01d_vector.svg", {}), ("01d_vector.pdf", {})]:
    fig.savefig(out / name, bbox_inches="tight", **kwargs)
    size = (out / name).stat().st_size / 1024
    pixels = f"{int(6 * kwargs['dpi'])} px wide" if "dpi" in kwargs else "vector (sharp at any zoom)"
    print(f"  {name:<18} {size:7.1f} KB  {pixels}")
plt.close(fig)

# ---------------------------------------------------------------- 5. why OO wins with several charts
print("\n=== 5. With several axes, OO avoids 'which chart am I on?' confusion ===")
fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))
left.plot(x, np.sin(x), color="tab:blue")
left.set_title("left.set_title(...)")
right.plot(x, x ** 2, color="tab:green")
right.set_title("right.set_title(...)")
plt.title("plt.title() hits only the CURRENT axes (the last one created)", color="red", fontsize=9)
print("  plt.title() changed:", repr(right.get_title()), "<- not the left one")
save_and_show(fig, "01e_oo_multiple_axes.png")
