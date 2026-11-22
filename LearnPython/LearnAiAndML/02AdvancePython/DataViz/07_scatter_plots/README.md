# Lecture 07: Scatter plots

Run: `python lecture.py`

## What a scatter plot shows

**One dot per record**, with x = one variable and y = another. It reveals **relationships**:

| Pattern | Meaning |
|---------|---------|
| dots rise left → right | positive relationship (more study → higher score) |
| dots fall | negative relationship |
| shapeless cloud | no (linear) relationship |
| curve | non-linear relationship (a line fit would mislead) |
| separate clumps | clusters / groups |
| lone dots far away | outliers |

## The call

```python
ax.scatter(x, y, s=40, c="tab:blue", alpha=0.6, edgecolor="k", marker="o")
```

| Argument | Encodes / does |
|----------|----------------|
| `s` | marker **size** (area in points²): a constant, or an array to encode a 3rd variable ("bubble chart") |
| `c` | colour: one colour, or an **array of numbers** + `cmap="viridis"` to encode a variable |
| `cmap`, `vmin`, `vmax`, `norm` | the colour mapping |
| `alpha` | transparency: essential with many points |
| `edgecolor` / `linewidths` | marker outline |
| `marker` | `"o"`, `"s"`, `"^"`, `"x"`… |

`fig.colorbar(sc, ax=ax, label="...")` adds the colour key; `sc` is what `ax.scatter` returned.

For **categorical colour** (gender, class), loop over the groups with one `scatter` call and a `label` per group (or use Seaborn's `hue=`, Lecture 10).

## Trend line and correlation

```python
slope, intercept = np.polyfit(x, y, 1)     # least-squares straight line
r = df["x"].corr(df["y"])                  # Pearson correlation, from -1 to +1
```

| r | Strength |
|---|----------|
| ±0.9–1.0 | very strong |
| ±0.7–0.9 | strong |
| ±0.4–0.7 | moderate |
| ±0.1–0.4 | weak |
| ~0 | no *linear* relationship (there may still be a curve!) |

> **Correlation ≠ causation.** Ice-cream sales and drownings rise together because of summer, not because one causes the other.

## Overplotting: when there are too many dots

With thousands of points, dots pile up into a solid blob, and you can't see where most of the data is.

| Fix | How |
|-----|-----|
| transparency | `alpha=0.1` |
| smaller markers | `s=2` |
| **hexbin** | `ax.hexbin(x, y, gridsize=30, cmap="viridis")`: counts per hexagon |
| 2-D histogram / KDE | `hist2d` (Lecture 06), `sns.kdeplot(x=, y=)` (Lecture 11) |
| sampling | plot a random 10% |

## Labelling points

`ax.annotate(name, (x, y), xytext=(5, 5), textcoords="offset points")` labels interesting points (outliers, top performers). Label only a few.

## Exercises

1. Add a quadratic trend line with `np.polyfit(x, y, 2)` and compare it with the straight line.
2. Colour the points by grade level (one `scatter` per group, with a legend).
3. Label the 3 students with the highest score.
4. Make 50,000 random points and compare a plain scatter, `alpha=0.05`, and `hexbin`.

**Next →** [Lecture 08: Subplots & layouts](../08_subplots_and_layouts/)
