# Lecture 10: Introduction to Seaborn

Run: `python lecture.py`

## What Seaborn is

**Seaborn** is a statistical plotting library **built on top of Matplotlib**. You describe *what* you want ("score vs study hours, coloured by gender"), and Seaborn handles the grouping, colours, legend, aggregation and confidence intervals.

```python
import seaborn as sns
sns.set_theme(style="whitegrid")
sns.scatterplot(data=df, x="study_hours", y="score", hue="gender")
```

## Why use it?

| Matplotlib | Seaborn |
|------------|---------|
| you loop over groups and build the legend yourself | `hue="gender"` does it |
| you compute means/CIs before plotting | `barplot`, `lineplot` aggregate automatically |
| works with arrays | works directly with **DataFrame column names** |
| plain defaults | attractive themes and palettes |
| total control | less control, so finish with Matplotlib calls |

They work **together**: every Seaborn axes-level function returns a Matplotlib `Axes`, so you can call `ax.set_title(...)` and anything else you learned in Lectures 01–09.

## Semantic mappings: the big idea

Most Seaborn functions map **columns** to visual properties:

| Parameter | Maps a column to | Example |
|-----------|------------------|---------|
| `x`, `y` | position | `x="study_hours"` |
| `hue` | **colour** | `hue="gender"` |
| `style` | marker / line style | `style="grade_level"` |
| `size` | marker size / line width | `size="sleep_hours"` |
| `col`, `row` | **separate subplots** (figure-level functions only) | `col="grade_level"` |

## Data format: long ("tidy") vs wide

Seaborn works best with **long / tidy data**: one row per observation, one column per variable.

| Wide (one column per category) | Long (tidy) |
|--------------------------------|-------------|
| `Month, Electronics, Clothing, Groceries` | `Month, Category, Sales` |
| 12 rows | 36 rows |

Convert with pandas: `long = wide.melt(id_vars="Month", var_name="Category", value_name="Sales")`, and back with `pivot`. Then `hue="Category"` works.

## Axes-level vs figure-level functions

| | Axes-level | Figure-level |
|--|------------|--------------|
| examples | `scatterplot`, `lineplot`, `histplot`, `kdeplot`, `boxplot`, `barplot`, `heatmap` | `relplot`, `displot`, `catplot`, `lmplot`, `pairplot`, `jointplot` |
| draws into | one Matplotlib `Axes` (pass `ax=` to place it in your subplots) | its **own** figure; can make a grid with `col=` / `row=` |
| returns | `Axes` | a `FacetGrid` / `PairGrid` / `JointGrid` (`g.figure`, `g.axes`) |
| size | `figsize` of your figure | `height=` and `aspect=` per panel |
| title | `ax.set_title()` | `g.figure.suptitle(..., y=1.02)` |

| Axes-level | Its figure-level family |
|------------|-------------------------|
| `scatterplot`, `lineplot` | `relplot(kind="scatter" / "line")` |
| `histplot`, `kdeplot`, `ecdfplot` | `displot(kind="hist" / "kde" / "ecdf")` |
| `stripplot`, `boxplot`, `barplot`… | `catplot(kind="strip" / "box" / "bar" …)` |
| `regplot` | `lmplot` |

## Themes in one line

`sns.set_theme(style="whitegrid", palette="deep", context="notebook")`

- styles: `darkgrid` (default), `whitegrid`, `dark`, `white`, `ticks`
- contexts (overall scale): `paper` < `notebook` < `talk` < `poster`

More in Lecture 15.

## Exercises

1. Recreate the Matplotlib grouped scatter in Seaborn and add `style="grade_level"`.
2. Melt the sales data and draw all three categories with one `sns.lineplot` call.
3. Use `sns.relplot(..., col="grade_level", col_wrap=2)` to make one panel per grade.
4. Take the `Axes` returned by `sns.scatterplot` and add a Matplotlib annotation to it.

**Next →** [Lecture 11: Distributions](../11_seaborn_distributions/)
