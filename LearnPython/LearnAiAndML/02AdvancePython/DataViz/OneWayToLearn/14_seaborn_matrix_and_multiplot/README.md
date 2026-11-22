# Lecture 14: Matrix plots & multi-plot grids

Run: `python lecture.py`

## Heatmaps: a table of numbers as colours

```python
sns.heatmap(table, annot=True, fmt=".1f", cmap="YlGnBu", linewidths=0.5, cbar_kws={"label": "Sales"})
```

The input is a **2-D table**: a DataFrame (its index and columns become the labels) or a 2-D array. Typical sources:

| Source | Code |
|--------|------|
| correlation matrix | `df[num_cols].corr()` |
| pivot table | `df.pivot_table(index="region", columns="quarter", values="sales", aggfunc="sum")` |
| cross-tab counts | `pd.crosstab(df["day"], df["time"])` |
| confusion matrix | from scikit-learn |

| Parameter | Effect |
|-----------|--------|
| `annot=True`, `fmt=".2f"` / `"d"` / `".0%"` | print values in cells |
| `cmap` | **sequential** (`"YlGnBu"`, `"viridis"`) for magnitudes; **diverging** (`"coolwarm"`, `"RdBu_r"`) when there's a meaningful centre |
| `center=0`, `vmin=-1, vmax=1` | fix the colour scale (correlations!) |
| `mask=np.triu(np.ones_like(corr, bool))` | hide the redundant upper triangle of a correlation matrix |
| `square=True`, `linewidths`, `linecolor` | cell layout |
| `cbar=False` | no colourbar |

`sns.clustermap` reorders rows and columns so similar ones sit together (hierarchical clustering). It's great for spotting groups.

## Pair plots: every numeric pair at once

```python
sns.pairplot(df, vars=["study_hours", "sleep_hours", "score"], hue="gender", corner=True)
```

- The diagonal shows each variable's distribution (`diag_kind="kde"` or `"hist"`).
- Off-diagonal cells show scatter plots (`kind="reg"` adds fitted lines, `"kde"` gives contours).
- `corner=True` drops the duplicate upper half.
- `PairGrid` gives full control: `g.map_upper(...)`, `g.map_lower(...)`, `g.map_diag(...)`.

It's the classic **first look at a new dataset**: you see distributions, relationships and group separation in one figure. With many columns it gets slow and tiny, so pick 3–6 variables.

## Joint plots: two variables + their distributions

```python
sns.jointplot(data=df, x="study_hours", y="score", kind="reg")    # "scatter", "kde", "hex", "hist", "resid"
```

The centre shows the relationship; the margins show each variable's distribution. `JointGrid` gives custom combinations (`g.plot_joint(...)`, `g.plot_marginals(...)`).

## FacetGrid: your own small multiples

```python
g = sns.FacetGrid(df, col="grade_level", row="gender", col_order=[...], height=3)
g.map_dataframe(sns.histplot, x="score", binwidth=10)
g.set_axis_labels("Score", "Count")
g.set_titles("{row_name} | {col_name}")
g.add_legend()
```

`relplot`, `displot`, `catplot` and `lmplot` build a `FacetGrid` for you. Use one directly when you want to map **any** plotting function, including your own.

| Grid object | Made by | Useful attributes |
|-------------|---------|-------------------|
| `FacetGrid` | `relplot`, `displot`, `catplot`, `lmplot`, or directly | `g.figure`, `g.axes`, `g.axes_dict`, `g.set_titles`, `g.refline(y=...)` |
| `PairGrid` | `pairplot` | `g.map_upper/lower/diag` |
| `JointGrid` | `jointplot` | `g.ax_joint`, `g.ax_marg_x`, `g.ax_marg_y` |

## Exercises

1. Make a pivot-table heatmap of sales by region × quarter, annotated in lakh.
2. Plot the lower-triangle correlation heatmap of the restaurant data's numeric columns.
3. Build a `PairGrid` with scatter plots below, KDE contours above and histograms on the diagonal.
4. Use `FacetGrid` with `row="time", col="day"` and `map_dataframe(sns.scatterplot, ...)`.

**Next →** [Lecture 15: Themes & palettes](../15_seaborn_themes_and_palettes/)
