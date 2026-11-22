# Lecture 03: Bar charts

Run: `python lecture.py`

## When to use bars

Bars encode a value as **length**, which the eye compares very accurately. Use them to **compare categories**: sales per product, students per grade, revenue per region.

| Variant | Use when |
|---------|----------|
| vertical `ax.bar` | few categories, short labels, or ordered categories (months) |
| horizontal `ax.barh` | **long category names**, many categories, rankings |
| grouped | compare **sub-groups** side by side (category × month) |
| stacked | show **totals and their composition** together |
| 100% stacked | compare **shares** between groups |
| with error bars | means with uncertainty |

## Core calls

```python
bars = ax.bar(x, height, width=0.8, color=..., edgecolor=..., label=...)
ax.barh(y, width)                          # horizontal: categories on the y-axis
ax.bar_label(bars, fmt="%.0f", padding=3)  # write each value on its bar
```

## Grouped bars: shift each series

Bars are drawn at numeric positions, so **shift** each series by one bar width:

```python
x = np.arange(len(months))      # [0, 1, 2, ...] group centres
w = 0.27
ax.bar(x - w, electronics, w, label="Electronics")
ax.bar(x,     clothing,    w, label="Clothing")
ax.bar(x + w, groceries,   w, label="Groceries")
ax.set_xticks(x, months)        # put readable labels back at the centres
```

## Stacked bars: use `bottom=`

Each new series starts where the previous one ended:

```python
ax.bar(x, a, label="A")
ax.bar(x, b, bottom=a, label="B")
ax.bar(x, c, bottom=a + b, label="C")
```

For **100% stacked**, divide each row by its total first. (`ax.barh` uses `left=` instead of `bottom=`.)

## Error bars

`ax.bar(x, means, yerr=std, capsize=4)` draws a line from mean − err to mean + err. Say what the error bar represents (standard deviation, standard error or a 95% CI) in the caption.

## Design rules

| Rule | Why |
|------|-----|
| **Start the value axis at 0** | bar length *is* the value; a truncated axis exaggerates differences (Lecture 16) |
| **Sort** bars by value (unless the order is natural, like months) | rankings become instantly readable |
| Horizontal bars for long labels | no rotated, unreadable text |
| Label values directly (`bar_label`) and drop the gridlines | less eye travel |
| Highlight one bar with colour, grey the rest | focuses attention |
| ≤ 3–4 series in grouped bars | otherwise split into subplots |

**Bar chart vs histogram:** bars compare *categories* (with gaps). A histogram shows a *continuous* variable's distribution (adjacent bins, no gaps), covered in Lecture 06.

## Exercises

1. Make a stacked bar chart of the three categories for Jan–Jun with value labels in each segment (`label_type="center"`).
2. Turn the horizontal chart into a ranking of all 12 months' Electronics sales, highlighting the best month.
3. Add error bars of ±10% to the simple bar chart.
4. Make a 100% stacked horizontal bar chart of the categories by quarter.

**Next →** [Lecture 04: Pie & donut charts](../04_pie_and_donut_charts/)
