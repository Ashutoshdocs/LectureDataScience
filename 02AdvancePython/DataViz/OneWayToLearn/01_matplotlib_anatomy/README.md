# Lecture 01: Matplotlib anatomy: Figure, Axes and the two interfaces

Run: `python lecture.py`

## Why learn the anatomy first?

Every Matplotlib question ("how do I rotate labels?", "why is my title on the wrong chart?") becomes easy once you know **which object** you're talking to.

## The parts of a chart

```
┌───────────────────────── Figure ──────────────────────────┐   the whole canvas / window / image file
│  suptitle                                                 │
│  ┌──────────────────── Axes ─────────────────────────┐    │   ONE plot area (a figure can hold many)
│  │ title                                    legend   │    │
│  │  y-axis ─┐   ── line (Line2D artist)              │    │
│  │  ticks   │   ●  markers                           │    │
│  │  label   │   ▮  bars (Rectangle artists)          │    │
│  │          └──────────── x-axis, ticks, label ──────│    │
│  └───────────────────────────────────────────────────┘    │
└───────────────────────────────────────────────────────────┘
```

| Object | What it is | You use it to… |
|--------|------------|----------------|
| **Figure** (`fig`) | the whole canvas | set the size, overall title (`fig.suptitle`), save (`fig.savefig`), add colourbars |
| **Axes** (`ax`) | one plot area with its own coordinate system. ⚠️ *not* the plural of "axis" | draw (`ax.plot`, `ax.bar`), title, labels, limits, legend |
| **Axis** (`ax.xaxis`, `ax.yaxis`) | the number line with ticks | tick positions, formats |
| **Artist** | *everything* drawn: lines, text, rectangles, ticks | style individual elements (`line.set_color("red")`) |

## Two ways to write Matplotlib code

### 1. pyplot (state-based, MATLAB-style)

```python
plt.figure()
plt.plot(x, y, label="sin")
plt.title("...")
plt.legend()
plt.show()
```

`plt.*` functions act on the **"current" figure and axes**, which Matplotlib tracks for you (`plt.gcf()`, `plt.gca()`). This is quick for one-off plots in a notebook.

### 2. Object-oriented (OO), recommended

```python
fig, ax = plt.subplots()
ax.plot(x, y, label="sin")
ax.set_title("...")
ax.legend()
fig.savefig("chart.png")
```

You hold **explicit references**, so there's no confusion about which chart gets the title. It's essential for subplots and functions that build charts.

| pyplot | OO equivalent |
|--------|---------------|
| `plt.title()` | `ax.set_title()` |
| `plt.xlabel()` / `plt.ylabel()` | `ax.set_xlabel()` / `ax.set_ylabel()` |
| `plt.xlim()` / `plt.ylim()` | `ax.set_xlim()` / `ax.set_ylim()` |
| `plt.xticks()` | `ax.set_xticks()` |
| `plt.legend()`, `plt.plot()` | `ax.legend()`, `ax.plot()` |
| `plt.savefig()` | `fig.savefig()` |

Rule: setters on `ax` start with `set_`. **Use the OO style in this course from now on.**

## Figure size, DPI and saving

```python
fig, ax = plt.subplots(figsize=(9, 5))        # width, height in INCHES
fig.savefig("chart.png", dpi=150, bbox_inches="tight")
```

| Option | Meaning |
|--------|---------|
| `figsize=(w, h)` | size in inches |
| `dpi` | dots per inch: pixels = inches × dpi (9 × 150 = 1350 px wide) |
| format | taken from the extension: `.png` (web, slides), `.svg` / `.pdf` (vector: sharp at any zoom, for print), `.jpg` |
| `bbox_inches="tight"` | trims extra white space so labels aren't cut off |
| `transparent=True` | transparent background |

`plt.show()` opens a window and **blocks** until you close it. Call `savefig` **before** `show`, because after the window closes the figure may be empty. `plt.close(fig)` frees memory; creating hundreds of figures without closing them triggers a warning.

## Exercises

1. Recreate the sin/cos chart with the OO interface.
2. Save the same figure as PNG at dpi 72 and 300, and as SVG. Compare the file sizes.
3. Use `fig, ax = plt.subplots()` and print `type(fig)`, `type(ax)`, `type(ax.xaxis)`.
4. Draw a line, keep the returned object (`line, = ax.plot(...)`), then change its colour with `line.set_color("red")`.

**Next →** [Lecture 02: Line plots](../02_line_plots/)
