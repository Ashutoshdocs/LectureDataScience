# Lecture 19: Plotting with pandas

Run: `python lecture.py`. Charts are saved as PNG files in `output/`.

Every Series and DataFrame has a `.plot()` method built on **Matplotlib**. One line turns a summary into a chart.

```python
monthly.plot(kind="line", title="Revenue by month")
```

## Chart types: `kind=`

| `kind` | Use for | Example |
|--------|---------|---------|
| `"line"` | change over time | monthly revenue |
| `"bar"` / `"barh"` | comparing categories | revenue by region |
| `"bar", stacked=True` | parts of a whole per category | region × category |
| `"hist"` | distribution of one number | order sizes |
| `"box"` | spread & outliers by group | marks per subject |
| `"scatter"` | relationship between two numbers | maths vs science |
| `"pie"` | share of a whole (few slices only) | category share |
| `"area"` | stacked totals over time | category revenue over months |

Shortcuts: `df.plot.bar()`, `df.plot.hist()` and so on.

## The recipe

1. **Summarise first** (groupby / pivot / resample). Plot the result, not 240 raw rows.
2. Sort bars so the chart reads at a glance: `.sort_values()`.
3. Add a title and axis labels: `title=`, `xlabel=`, `ylabel=`.
4. Save: `ax.figure.savefig("chart.png", dpi=150, bbox_inches="tight")`.

```python
import matplotlib.pyplot as plt

ax = sales.groupby("region")["revenue"].sum().sort_values().plot(
        kind="barh", title="Revenue by region", xlabel="Revenue (Rs)")
ax.figure.savefig("output/region.png", dpi=150, bbox_inches="tight")
plt.close(ax.figure)
```

## Useful options

| Option | Does |
|--------|------|
| `figsize=(8, 4)` | size in inches |
| `title=`, `xlabel=`, `ylabel=` | labels |
| `legend=False` | hide legend |
| `grid=True` | gridlines |
| `rot=0` | rotate x tick labels |
| `subplots=True` | one chart per column |
| `color="#2f62c9"` | a single colour |
| `logy=True` | log scale |

## Showing vs saving

- In a **script**, call `plt.show()` to open a window, or `savefig` to write a file.
- In **Jupyter**, charts appear automatically under the cell.
- `plt.close()` after saving frees memory when you make many charts.

## Going further

- **seaborn**: nicer statistical charts that accept DataFrames directly
- **plotly**: interactive charts (`df.plot(backend="plotly")`)

## Exercises

1. Bar chart of units sold per product, sorted.
2. Histogram of order revenue with 20 bins.
3. Box plot of marks per subject from `students.csv`.
4. Line chart of weekly order counts.

<details><summary>Solutions</summary>

```python
sales.groupby("product")["units"].sum().sort_values().plot.barh()
sales["revenue"].plot.hist(bins=20)
students[["maths", "science", "english", "cs"]].plot.box()
sales.set_index("date")["order_id"].resample("W").count().plot()
```
</details>

**Next →** [Lecture 20: Project, sales analysis](../20_project_sales_analysis/)
