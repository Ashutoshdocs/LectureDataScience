# Lecture 15: Themes, contexts & colour palettes

Run: `python lecture.py`

## `sns.set_theme()`: one call for the whole look

```python
sns.set_theme(style="whitegrid", palette="deep", context="notebook", font_scale=1.1, rc={"axes.spines.top": False})
```

It changes Matplotlib's global defaults, so it affects plain Matplotlib charts too. Call `sns.reset_defaults()` (or `plt.rcdefaults()`) to undo it.

### Styles: background and grid

| Style | Look | Good for |
|-------|------|----------|
| `darkgrid` (Seaborn's default) | grey background, white grid | exploration |
| `whitegrid` | white background, grey grid | reading values, reports |
| `white` | no grid | clean charts, annotations |
| `dark` | grey, no grid | |
| `ticks` | white + tick marks | publications; combine with `sns.despine()` |

`sns.despine()` removes the top/right spines (`left=True` too, `offset=10` to detach the axes). `with sns.axes_style("white"):` applies a style temporarily.

### Contexts: scale for the destination

| Context | Use |
|---------|-----|
| `paper` | smallest: documents |
| `notebook` | default |
| `talk` | slides |
| `poster` | largest: posters, big screens |

`sns.set_context("talk", font_scale=1.2)` scales fonts, line widths and markers **together**.

## Colour palettes: match the palette to the data

| Data | Palette type | Examples |
|------|--------------|----------|
| **categories** (no order) | **qualitative** | `"deep"` (default), `"muted"`, `"pastel"`, `"bright"`, `"dark"`, `"colorblind"`, `"Set2"`, `"tab10"` |
| **ordered / numeric** (low → high) | **sequential** | `"rocket"`, `"mako"`, `"viridis"`, `"Blues"`, `"light:seagreen"`, `"dark:salmon_r"` |
| values around a **meaningful centre** | **diverging** | `"vlag"`, `"icefire"`, `"coolwarm"`, `"RdBu"` |

```python
sns.color_palette("deep")                     # a list of RGB colours
sns.color_palette("rocket", n_colors=5)
sns.color_palette("blend:#7AB,#EDA", 5)       # your own gradient
sns.color_palette("husl", 8)                  # evenly spaced hues
sns.set_palette("colorblind")                 # make it the default
palette={"Male": "tab:blue", "Female": "tab:pink"}   # exact colours per category
```

Pass `palette=` to any Seaborn function. For numeric `hue`, Seaborn uses a sequential palette automatically.

## Accessibility: colour-blind-safe charts

About 1 in 12 men and 1 in 200 women have some colour-vision deficiency, most often red–green.

1. Prefer `"colorblind"`, `viridis`-family or blue/orange palettes. Avoid relying on red vs green alone.
2. **Don't rely on colour alone**: add markers (`style=`), line dashes, direct labels or patterns.
3. Check that the chart still works in **greyscale**: sequential palettes should vary in *lightness*.
4. Use ≤ 6–8 distinct categorical colours. Beyond that, group or facet.

## Brand colours

Define them once and reuse them: `BRAND = ["#0B5394", "#E69138", "#6AA84F", "#999999"]`, `sns.set_palette(BRAND)`.

## Exercises

1. Render one chart in all five styles.
2. Make the same bar chart in `paper`, `talk` and `poster` contexts and save each one.
3. Plot a 9-category bar chart with `"deep"` vs `"husl"` vs a sequential palette. Which one misleads?
4. Rebuild a red/green line chart so that it works for colour-blind readers.

**Next →** [Lecture 16: Choosing charts & common mistakes](../16_choosing_charts_and_common_mistakes/)
