# Lecture 08: Subplots & layouts

Run: `python lecture.py`

## Why several charts in one figure?

- **Dashboards**: several views of the same data together.
- **Small multiples**: the *same* chart for each group (one per region or category), which is often clearer than one crowded chart.
- **Comparisons** side by side with shared scales.

## `plt.subplots(rows, cols)`

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 1].bar(...)         # 2-D array: axes[row, col]
```

| You ask for | `axes` is | Access |
|-------------|-----------|--------|
| `subplots()` | a single Axes | `ax` |
| `subplots(1, 3)` or `(3, 1)` | 1-D array | `axes[0]`, or unpack: `fig, (a, b, c) = ...` |
| `subplots(2, 3)` | 2-D array | `axes[1, 2]` |
| any grid | | `for ax in axes.flat:` loops over all of them |

### Useful options

| Option | Effect |
|--------|--------|
| `sharex=True` / `sharey=True` | same scale on every subplot (essential for fair comparisons); inner tick labels hidden |
| `sharey="row"` | share within each row |
| `figsize=(w, h)` | grow the figure with the number of subplots |
| `layout="constrained"` | automatic spacing that also handles colourbars and suptitles (a modern alternative to `tight_layout`) |
| `gridspec_kw={"width_ratios": [2, 1]}` | unequal sizes |
| `fig.suptitle("...")` | one overall title |
| `fig.supxlabel` / `fig.supylabel` | one shared axis label |
| `ax.remove()` / `ax.set_visible(False)` | hide unused cells in a grid |

## Uneven layouts

### GridSpec

```python
gs = fig.add_gridspec(2, 2)
top = fig.add_subplot(gs[0, :])      # row 0, all columns
left = fig.add_subplot(gs[1, 0])
right = fig.add_subplot(gs[1, 1])
```

Slicing (`gs[0, :]`, `gs[:, 0]`, `gs[1:, 1:]`) lets one chart span several cells.

### `subplot_mosaic`: the most readable way

```python
fig, ax = plt.subplot_mosaic([["trend", "trend", "share"],
                              ["hist",  "scatter", "share"]], figsize=(14, 8))
ax["trend"].plot(...)               # access by NAME
```

Each name is one Axes. Repeat a name to make it span cells. Use `"."` for an empty cell.

## Insets and twin axes

- `ax.inset_axes([x0, y0, width, height])` (fractions of the parent Axes) puts a small zoomed chart *inside* another.
- `ax.twinx()` adds a second y-axis (Lecture 02).

## Small multiples beat spaghetti

Twelve lines on one chart are unreadable. Twelve small charts with **shared axes** are easy to compare. `lecture.py` shows both.

## Exercises

1. Build a 3×2 dashboard with six different chart types (your original practice idea).
2. Make small multiples of the three sales categories with `sharey=True`, then with `sharey=False`. Which comparison does each version make easier?
3. Recreate the GridSpec layout with `subplot_mosaic`.
4. Add an inset that zooms into Jan–Mar of a line chart.

**Next →** [Lecture 09: Customization & styling](../09_customization_and_styling/)
