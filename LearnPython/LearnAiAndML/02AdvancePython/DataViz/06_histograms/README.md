# Lecture 06: Histograms

Run: `python lecture.py`

## What a histogram shows

It splits a **continuous numeric variable** into ranges (**bins**) and counts how many values fall into each. You see the **shape of the distribution**:

| Shape | Looks like | Example |
|-------|------------|---------|
| symmetric / bell-shaped | one peak in the middle | heights, exam scores |
| right-skewed | long tail to the right | incomes, house prices, waiting times |
| left-skewed | long tail to the left | age at retirement |
| bimodal | two peaks | mixture of two groups (e.g. weekday vs weekend traffic) |
| uniform | flat | random numbers, study hours in our dataset |
| outliers | isolated bars far away | data errors, VIPs |

**Histogram vs bar chart:** a bar chart compares *categories* (with gaps between bars). A histogram shows how *one continuous variable* is spread (adjacent bins, no gaps).

## The call

```python
counts, edges, patches = ax.hist(data, bins=15, color="slateblue", edgecolor="white")
```

It returns the counts per bin, the bin edges, and the bar artists.

| Argument | Effect |
|----------|--------|
| `bins=15` | number of equal-width bins |
| `bins=range(0, 101, 5)` | **explicit edges**, essential when comparing groups (same bins!) |
| `bins="auto"` / `"fd"` / `"sturges"` | let NumPy choose |
| `range=(0, 100)` | limit the range |
| `density=True` | area sums to 1, so the y-axis is **density**, not counts; needed to compare groups of different sizes |
| `cumulative=True` | running total ("how many scored *at most* x?") |
| `histtype="step"` | outline only: great for overlaying several groups |
| `alpha=0.6` | transparency for overlapping filled histograms |
| `orientation="horizontal"` | sideways |
| `weights=` | weight each value |

## Choosing the number of bins

Too **few** bins hide the shape (everything becomes one blob). Too **many** create noise (random spikes and gaps). Start with `bins="auto"` or 10–30, then try a few values. `lecture.py` shows 5 vs 15 vs 50, and a case where 5 bins hide a bimodal distribution entirely.

## Adding context

- `ax.axvline(mean, ls="--")` and `ax.axvline(median, ls=":")`: if mean > median, the data is right-skewed.
- Shade a pass/fail threshold with `ax.axvspan`.

## Comparing groups

| Approach | Good for |
|----------|----------|
| overlapping, `alpha=0.5`, **same bins** | 2 groups |
| `histtype="step"` outlines | 2–4 groups |
| `density=True` | groups of different sizes |
| small multiples (one subplot per group, `sharex=True`) | many groups |
| box/violin plots (Lecture 12) or KDE (Lecture 11) | many groups, compact |

## 2-D histograms

`ax.hist2d(x, y, bins=30)` or `ax.hexbin(x, y, gridsize=25)` count points in 2-D cells, which solves overplotting in big scatter plots (Lecture 07).

## Exercises

1. Add `density=True` to the basic histogram. What changed on the y-axis, and what stayed the same?
2. Plot a cumulative histogram and read off how many students scored below 50.
3. Compare the scores of the four grade levels as `step` histograms.
4. Generate 10,000 incomes with `np.random.default_rng(0).lognormal(10, 0.6, 10_000)`, then plot their histogram and the histogram of their log.

**Next →** [Lecture 07: Scatter plots](../07_scatter_plots/)
