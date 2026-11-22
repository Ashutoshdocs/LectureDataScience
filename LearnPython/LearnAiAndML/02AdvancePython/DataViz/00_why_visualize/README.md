# Lecture 00: Why visualize data?

Run: `python lecture.py` → charts in `output/`

## What you need first

- Python basics, and **pandas** basics: a DataFrame, selecting a column `df["col"]`, `df.describe()`
- **NumPy** arrays: `np.arange`, `np.linspace`
- Install the libraries: `pip install -r ../requirements.txt`

## What is data visualization?

**Turning numbers into pictures** so that patterns, trends, comparisons and outliers become obvious at a glance.

## Why it matters

| Reason | Example |
|--------|---------|
| **Speed** | the eye spots a rising line instantly but struggles with a table of 36 numbers (try it in `lecture.py`) |
| **Patterns** | seasonality, clusters, correlations |
| **Outliers & errors** | a negative age or a sensor spike jumps out of a chart; it hides in a table |
| **Summary statistics can lie** | **Anscombe's quartet**: four datasets with the *same* mean, variance, correlation and regression line look completely different when plotted |
| **Communication** | managers and clients understand a good chart faster than a paragraph |

> "The greatest value of a picture is when it forces us to notice what we never expected to see." (John Tukey)

## Two purposes of a chart

| Exploratory (for you) | Explanatory (for others) |
|-----------------------|--------------------------|
| quick, many charts, rough | few charts, polished |
| "what's in this data?" | "here is the one point I want you to see" |
| defaults are fine | titles, labels, annotations, highlight colours |

## Every good chart has…

1. A **title** that says what the chart shows (ideally the insight: "Electronics sales doubled in 2026").
2. **Axis labels with units** ("Sales (₹ thousands)").
3. A **legend** whenever there's more than one series.
4. A sensible **scale**. Bars must start at 0.
5. **No clutter**: remove anything that doesn't help.

## Choosing a chart: the quick guide

| Goal | Chart | Lecture |
|------|-------|---------|
| trend over time | **line** | 02 |
| compare categories | **bar** (horizontal for long names) | 03 |
| parts of a whole (few parts) | pie / donut, stacked bar | 04, 03 |
| composition over time | **stack plot** | 05 |
| distribution of one variable | **histogram**, KDE, box plot | 06, 11, 12 |
| relationship between two variables | **scatter** | 07 |
| many variables at once | pair plot, heatmap | 14 |
| compare groups' distributions | box / violin plot | 12 |

Lecture 16 covers this in depth, with bad vs fixed examples.

## Matplotlib vs Seaborn

| | Matplotlib | Seaborn |
|--|------------|---------|
| level | low-level: full control of every element | high-level, built **on top of** Matplotlib |
| best for | any custom chart, dashboards, publication figures | statistical charts straight from DataFrames |
| grouping by a column | you write a loop | `hue="column"` |
| you'll use it for | Lectures 01–09 | Lectures 10–15 |

You'll use both together: Seaborn draws, and Matplotlib fine-tunes.

## Exercises

1. Look at the printed table in `lecture.py` for 10 seconds. Which category peaks in which month? Now check the chart.
2. Compute `df.describe()` for the four Anscombe datasets. Are they really almost identical?
3. For each question, name the best chart: (a) the share of each payment method; (b) monthly visitors over 3 years; (c) does price relate to rating?; (d) how are delivery times spread?

<details><summary>Answers to 3</summary>
(a) bar or pie (few categories) · (b) line · (c) scatter · (d) histogram / box plot
</details>

**Next →** [Lecture 01: Matplotlib anatomy](../01_matplotlib_anatomy/)
