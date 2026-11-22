# Lecture 11: Seaborn distribution plots

Run: `python lecture.py`

"How are the values spread out?" These functions answer it for **one variable** (or two, as a 2-D density).

| Function | Shows | Best for |
|----------|-------|----------|
| `histplot` | binned counts (a histogram) | the default first look |
| `kdeplot` | a **smooth** estimated density curve | comparing shapes of several groups |
| `ecdfplot` | the cumulative proportion ≤ x | exact percentiles, comparing groups without choosing bins |
| `rugplot` | a tick for every value | small datasets, added to other plots |
| `displot` | figure-level wrapper (`kind="hist"/"kde"/"ecdf"`) | facets with `col=` / `row=` |

## `histplot`

```python
sns.histplot(data=df, x="score", bins=15, kde=True)
```

| Parameter | Effect |
|-----------|--------|
| `bins`, `binwidth`, `binrange` | bin control |
| `kde=True` | overlays a smooth curve |
| `hue="gender"` | one histogram per group |
| `multiple=` | `"layer"` (overlap, default), `"stack"`, `"dodge"` (side by side), `"fill"` (proportions) |
| `stat=` | `"count"` (default), `"frequency"`, `"probability"`/`"proportion"`, `"percent"`, `"density"` |
| `common_norm=False` | normalise each hue group separately (compare shapes of unequal-size groups) |
| `element="step"`, `fill=False` | outline style |
| `x=` and `y=` | a 2-D histogram (heat-coloured cells) |

## `kdeplot`: kernel density estimate

It places a small smooth bump on each data point and adds them up. The result is a smooth curve whose **area is 1**.

| Parameter | Effect |
|-----------|--------|
| `fill=True` | shade under the curve |
| `bw_adjust=0.5` / `2` | smoothness: smaller = wigglier (follows noise), larger = smoother (hides detail) |
| `cut=0` | don't extend the curve beyond the data range (e.g. scores can't be < 0) |
| `common_norm=False` | each group's area = 1 |
| `x=` and `y=` | 2-D contours (`levels=`, `fill=True`, `thresh=`) |

⚠️ KDE can **suggest values that can't exist** (a negative age) and smooth away real gaps. Always cross-check with a histogram.

## `ecdfplot`: empirical cumulative distribution

The y-value at x is "the share of data ≤ x". You can read the median (y = 0.5) and any percentile directly. No bins and no smoothing, so it's honest and excellent for comparing groups.

## `displot`: the figure-level version

```python
sns.displot(data=df, x="score", hue="gender", col="grade_level", kind="kde", fill=True, height=3)
```

## Choosing

| Question | Use |
|----------|-----|
| first look at one variable | `histplot(kde=True)` |
| compare shapes of 2–4 groups | `kdeplot(hue=, common_norm=False)` or `ecdfplot(hue=)` |
| "what % are below 50?" | `ecdfplot` |
| many groups | `displot(col=...)` or box/violin plots (Lecture 12) |
| two variables' joint density | `kdeplot(x=, y=)` or `histplot(x=, y=)` |

## Exercises

1. Compare `multiple="stack"`, `"dodge"` and `"fill"` for scores by gender.
2. Draw KDEs with `bw_adjust` 0.2, 1 and 3. Which one over-smooths?
3. From an ECDF, read off the share of students scoring below 50.
4. Draw a filled 2-D KDE of study hours vs score.

**Next →** [Lecture 12: Categorical plots](../12_seaborn_categorical/)
