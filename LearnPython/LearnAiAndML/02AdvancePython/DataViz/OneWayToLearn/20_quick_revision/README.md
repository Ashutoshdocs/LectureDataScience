# Lecture 20: Quick revision: Matplotlib & Seaborn on one page

Run: `python lecture.py` for a 20-question self-test (answers computed from real figures) plus a one-image "cheat sheet" gallery of every chart type.

## Matplotlib skeleton (object-oriented)

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(9, 5))          # Figure = canvas, Axes = one plot
ax.plot(x, y, color="tab:blue", ls="--", marker="o", lw=2, label="A")
ax.set_title("Insight as the title", loc="left")
ax.set_xlabel("x (units)"); ax.set_ylabel("y (units)")
ax.legend(); ax.set_ylim(0, None)
fig.savefig("chart.png", dpi=150, bbox_inches="tight")   # save BEFORE plt.show()
plt.show()
```

## Chart functions

| Goal | Matplotlib | Seaborn |
|------|------------|---------|
| trend | `ax.plot` | `sns.lineplot` (aggregates + CI) |
| compare categories | `ax.bar` / `ax.barh` (+ `bar_label`) | `sns.barplot`, `sns.countplot` |
| grouped / stacked bars | offsets + `width` / `bottom=` | `barplot(hue=)`, `histplot(multiple="stack")` |
| parts of a whole | `ax.pie` (`wedgeprops={"width": .4}` = donut) | – |
| composition over time | `ax.stackplot` | – |
| distribution | `ax.hist(bins=, density=)` | `histplot`, `kdeplot`, `ecdfplot`, `displot` |
| groups' distributions | `ax.boxplot`, `ax.violinplot` | `boxplot`, `violinplot`, `stripplot`, `swarmplot` |
| relationship | `ax.scatter(c=, s=)`, `np.polyfit` | `scatterplot(hue=, size=, style=)`, `regplot`, `lmplot` |
| many points | `ax.hexbin`, `ax.hist2d` | `kdeplot(x=, y=)`, `jointplot(kind="hex")` |
| tables / matrices | `ax.imshow` | `heatmap(annot=True)`, `clustermap` |
| all pairs | – | `pairplot`, `PairGrid` |
| small multiples | `plt.subplots(r, c, sharey=True)` | `relplot / displot / catplot(col=, row=)`, `FacetGrid` |

## Layout

`plt.subplots(2, 2)` → `axes[r, c]` · `sharex/sharey` · `fig.suptitle` · `layout="constrained"` · `fig.add_gridspec` + `gs[0, :]` · `plt.subplot_mosaic([["a", "a"], ["b", "c"]])` · `ax.twinx()` · `ax.inset_axes`

## Annotate & customise

`ax.annotate(text, xy, xytext, arrowprops=dict(arrowstyle="->"))` · `ax.axhline / axvline / axvspan / fill_between` · `ax.text(..., transform=ax.transAxes)` · `ax.spines[["top", "right"]].set_visible(False)` · `FuncFormatter`, `PercentFormatter` · `ax.set_yscale("log")` · `ax.tick_params(axis="x", rotation=45)` · `plt.style.use(...)` / `plt.rcParams`

## Seaborn essentials

- `sns.set_theme(style="whitegrid", palette="colorblind", context="notebook")`
- Data: **long/tidy** DataFrames + column names; `df.melt(...)` converts wide → long.
- Semantics: `x, y, hue, style, size` (+ `col, row` in figure-level functions).
- **Axes-level** (`ax=`, returns an Axes) vs **figure-level** (`relplot/displot/catplot/lmplot/pairplot/jointplot`, returns a grid; `height`, `aspect`, `g.figure.suptitle(..., y=1.02)`).
- Error bars: `errorbar=("ci", 95)` | `"sd"` | `"se"` | `None`.
- Palettes: qualitative for categories, sequential for magnitude, diverging around a centre.

## Golden rules

1. Pick the chart from the **question** (comparison, trend, composition, distribution, relationship).
2. **Bars start at zero**; sort categories; horizontal bars for long labels.
3. ≤ 5–6 colours/series; highlight one and grey the rest; use small multiples instead of spaghetti.
4. Title = insight, axis labels have units, numbers are formatted, sources are noted.
5. Avoid pies with many slices, 3-D, rainbow colormaps, and misleading dual axes.
6. Use colour-blind-safe palettes, and don't rely on colour alone.
7. Show the data, not only means (box/violin/strip).
8. Save at the right size and format for the destination.

← [Back to course map](../README.md)
