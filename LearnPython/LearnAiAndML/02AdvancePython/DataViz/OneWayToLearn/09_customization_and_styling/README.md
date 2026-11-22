# Lecture 09: Customization & styling

Run: `python lecture.py`

Defaults make *a* chart. Customization makes *your* chart **clear, on-brand and focused on the message**.

## Colours

| Way to specify | Example |
|----------------|---------|
| name | `"steelblue"`, `"tomato"` |
| default cycle | `"C0"`, `"C1"`… or `"tab:blue"`, `"tab:orange"`… |
| hex | `"#1f77b4"` |
| RGB(A) tuple | `(0.2, 0.4, 0.6)`, `(0.2, 0.4, 0.6, 0.5)` |
| grey level | `"0.7"` (a string from 0 to 1) |

**Highlight, don't decorate:** one strong colour for the point you're making, grey for everything else.

## Colormaps (for numeric values)

| Type | Use for | Examples |
|------|---------|----------|
| **sequential** | low → high | `viridis` (default, perceptually uniform, colour-blind friendly), `Blues`, `magma` |
| **diverging** | values around a meaningful centre (0, a target) | `coolwarm`, `RdBu`, `BrBG`; set `vmin=-x, vmax=x` |
| **qualitative** | categories (no order) | `tab10`, `Set2`, `Dark2` |
| ❌ `jet` / `rainbow` | avoid | not perceptually uniform, which creates fake boundaries; bad for colour-blind readers and greyscale printing |

`plt.colormaps["viridis"](np.linspace(0, 1, 5))` gives 5 colours from a map.

## Ticks and number formatting

```python
from matplotlib.ticker import FuncFormatter, PercentFormatter, StrMethodFormatter, MultipleLocator

ax.yaxis.set_major_formatter(StrMethodFormatter("₹{x:,.0f}"))   # ₹12,000
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))           # 0.25 -> 25%
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1000:.0f}k"))
ax.xaxis.set_major_locator(MultipleLocator(5))                   # a tick every 5
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.set_xticks(positions, labels)                                 # explicit ticks + labels
```

> **Currency symbols:** the ₹ sign only renders if the chart font contains it (for example `plt.rcParams["font.family"] = "DejaVu Sans"`, or "Nirmala UI" on Windows). Otherwise you get a box and a warning. `lecture.py` writes "Rs", which works everywhere.

## Spines, grid and background

```python
ax.spines[["top", "right"]].set_visible(False)    # cleaner, "open" look
ax.grid(axis="y", alpha=0.3); ax.grid(False)
ax.set_facecolor("#f7f7f7")
```

## Text, annotations and legends

| Tool | Notes |
|------|-------|
| `ax.set_title(text, loc="left", fontsize=14, fontweight="bold", pad=12)` | left-aligned titles read like headlines |
| `ax.text(x, y, s, ha=, va=, transform=ax.transAxes)` | `transform=ax.transAxes` means (0, 0) is bottom-left and (1, 1) is top-right of the axes, whatever the data |
| `ax.annotate(s, xy, xytext, arrowprops=dict(arrowstyle="->"))` | point at data |
| `bbox=dict(boxstyle="round", fc="white", ec="gray")` | a box behind text |
| `ax.legend(loc="upper left", ncols=3, frameon=False, title="...")` | |
| `ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15))` | legend **outside** the axes |
| mathtext | `r"$\mu = 52$"`, `r"$R^2$"` |

## Styles and `rcParams`

```python
print(plt.style.available)               # 'ggplot', 'fivethirtyeight', 'seaborn-v0_8-whitegrid', ...
plt.style.use("ggplot")                  # global
with plt.style.context("dark_background"):   # just for this block
    ...
plt.rcParams.update({"font.size": 12, "axes.spines.top": False})   # fine-grained defaults
plt.rcdefaults()                          # reset
```

`common.apply_style()` is simply a style + `rcParams` bundle, which is how teams keep every chart consistent.

## Exporting for different uses

| Destination | Settings |
|-------------|----------|
| slides / web | PNG, `dpi=150–200`, `bbox_inches="tight"` |
| print / papers | PDF or SVG (vector) |
| over coloured backgrounds | `transparent=True` |
| exact pixel size | `figsize = (pixels_w / dpi, pixels_h / dpi)` |

## The "declutter" checklist

1. Remove the top/right spines and heavy gridlines.
2. Label lines directly instead of using a legend box.
3. Format numbers (`₹1.2M`, `25%`), not `1200000.0`.
4. Use one highlight colour; grey the rest.
5. Write a title that states the insight; put the units in the axis labels.
6. Use a large enough font for the destination.

`lecture.py` takes a default chart and applies this checklist step by step.

## Exercises

1. Format a y-axis in lakhs (`₹12.5L`) with `FuncFormatter`.
2. Make a diverging heatmap-style bar chart of profit/loss with red negatives and green positives.
3. Render the same chart in three built-in styles with `plt.style.context`.
4. Put a legend below the chart in 4 columns.

**Next →** [Lecture 10: Intro to Seaborn](../10_intro_seaborn/)
