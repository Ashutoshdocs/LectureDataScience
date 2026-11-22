# Lecture 12: Seaborn categorical plots

Run: `python lecture.py`

One axis is a **category** (grade, day, gender), and the other is a number. Seaborn has three families:

| Family | Functions | Shows |
|--------|-----------|-------|
| **every observation** | `stripplot`, `swarmplot` | each data point |
| **distribution summary** | `boxplot`, `violinplot`, `boxenplot` | spread, median, quartiles, shape, outliers |
| **estimate** | `barplot`, `pointplot`, `countplot` | one number per category (mean, count) + uncertainty |

Figure-level wrapper: `catplot(kind="strip"/"swarm"/"box"/"violin"/"bar"/"point"/"count", col=..., row=...)`.

## Common parameters

| Parameter | Effect |
|-----------|--------|
| `x="grade_level", y="score"` | categories on x (swap them for horizontal) |
| `order=[...]` | **category order**: always set it for ordered categories (Freshman → Senior), otherwise you get the data's order |
| `hue="gender"`, `hue_order=` | a second categorical split |
| `dodge=True` | separate hue groups side by side |
| `palette=` | colours |
| `orient="h"` | horizontal |

## Estimates: `barplot`, `pointplot`, `countplot`

- `countplot(x="day")` counts the **rows** per category (like `value_counts`).
- `barplot(x="day", y="tip")` shows the **mean** per category (`estimator="median"` or `sum` also work) with an **error bar**.
  - `errorbar=("ci", 95)` (default): 95% bootstrap confidence interval for the mean
  - `errorbar="sd"`: standard deviation (the spread of the data)
  - `errorbar="se"`: standard error
  - `errorbar=None`: none
- `pointplot` shows the same estimate as dots joined by lines, which is great for comparing **how hue groups change across categories** (interactions).

⚠️ A bar of means **hides the distribution**. Two groups with the same mean can look completely different. Show the points or a box plot as well when it matters.

## Box plot: the five-number summary

```
   o            <- outliers (beyond 1.5 × IQR from the box)
   ┬            <- whisker: furthest point within 1.5 × IQR
 ┌─┴─┐  Q3 (75th percentile)
 │───│  median
 └─┬─┘  Q1 (25th percentile)          IQR = Q3 − Q1
   ┴
```

Compact and great for comparing **many groups**, but it can hide bimodality.

## Violin plot

A mirrored KDE on each side, plus a mini box inside. It shows the **shape** (two humps, skew). `split=True` with a 2-level `hue` shows two halves. `inner="quart"`, `"box"`, `"stick"` or `"point"` controls what's drawn inside. With little data, the KDE shape can mislead.

## Strip and swarm plots

`stripplot` draws every point with random **jitter**. `swarmplot` arranges the points so they don't overlap; it's beautiful for up to a few hundred points per category, but too slow and wide beyond that. A classic combination is `boxplot` + `stripplot` on top, showing the summary *and* the raw data.

## Which one?

| Situation | Use |
|-----------|-----|
| how many rows per category | `countplot` |
| compare means, small audience | `barplot` (say what the error bars are) |
| compare a hue across ordered categories | `pointplot` |
| compare distributions of many groups | `boxplot` |
| shape matters (bimodal?) | `violinplot` |
| small data, show everything | `swarmplot` / `stripplot` (+ box) |

## Exercises

1. Make a `barplot` of mean tip by day with `errorbar="sd"`, then with `("ci", 95)`. Why are they different?
2. Draw a violin plot of score by grade with `hue="gender", split=True`.
3. Overlay a `stripplot` on a `boxplot` (set `color="black", size=3`).
4. Use `catplot(kind="point", col="time")` for tips by day and smoker.

**Next →** [Lecture 13: Relational & regression plots](../13_seaborn_relational_and_regression/)
