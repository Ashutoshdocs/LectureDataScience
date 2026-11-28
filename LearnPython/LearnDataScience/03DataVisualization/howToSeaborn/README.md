# Seaborn: Complete Beginner-to-Advanced Teaching Guide

A practical course for learning **Seaborn** from the first statistical chart to multi-variable exploratory data analysis (EDA). It includes two runnable projects with sample CSV data.

## Learning outcomes

Students will learn to:
- Explain what Seaborn is and how it relates to Matplotlib, Pandas, and NumPy.
- Load and inspect datasets using Pandas.
- Understand long-form and wide-form data.
- Create relational, categorical, distribution, and regression plots.
- Use `hue`, `size`, and `style` to visualize additional variables.
- Customize themes, palettes, legends, axes, and figure layouts.
- Build multi-plot grids with `FacetGrid`, `PairGrid`, and `JointGrid`.
- Create correlation heatmaps and clustered visualizations.
- Perform exploratory data analysis and communicate findings.
- Combine Seaborn with Matplotlib for fine-grained customization.

---

# Part 1 — Foundations

## Chapter 1 — What is data visualization?

Data visualization represents data in a visual form so that people can identify:
- Trends over time.
- Differences between categories.
- Relationships between variables.
- Distributions and unusual observations.
- Patterns across multiple dimensions.

A good chart answers a question. The chart type should match the data and the question.

## Chapter 2 — What is Seaborn?

Seaborn is a Python statistical data visualization library built on top of Matplotlib. It provides a high-level interface for creating attractive statistical graphics and works naturally with Pandas DataFrames.

Use:
- **NumPy** for numerical arrays and calculations.
- **Pandas** for tabular data manipulation.
- **Seaborn** for statistical visualizations.
- **Matplotlib** for lower-level figure and axes customization.

Seaborn does not replace Matplotlib. Seaborn creates plots using Matplotlib objects, so you can customize a Seaborn chart with Matplotlib methods.

## Chapter 3 — Environment setup

### Windows PowerShell
```powershell
mkdir seaborn-course
cd seaborn-course
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install seaborn matplotlib pandas numpy
```

### Linux / macOS
```bash
mkdir seaborn-course
cd seaborn-course
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install seaborn matplotlib pandas numpy
```

Verify:
```bash
python -c "import seaborn as sns; print(sns.__version__)"
```

Install this toolkit's dependencies:
```bash
pip install -r requirements.txt
```

## Chapter 4 — Your first Seaborn chart

```python
import seaborn as sns
import matplotlib.pyplot as plt

tips = sns.load_dataset("tips")

sns.scatterplot(data=tips, x="total_bill", y="tip")
plt.title("Bill Amount vs Tip")
plt.show()
```

For a reproducible class or offline environment, use the CSV files included in this toolkit rather than relying on downloading built-in example datasets.

## Chapter 5 — Seaborn's relationship with Matplotlib

Seaborn provides convenient high-level plotting functions. Matplotlib gives direct access to the figure and axes.

```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df, x="study_hours", y="marks", ax=ax)
ax.set_title("Study Hours vs Marks")
ax.set_xlabel("Study hours")
ax.set_ylabel("Marks")
fig.tight_layout()
plt.show()
```

Passing `ax=ax` is useful when creating subplots or combining multiple charts in one figure.

## Chapter 6 — Long-form and wide-form data

**Long-form data** usually has one observation per row and separate columns for variables.

| student | subject | marks |
|---|---|---:|
| Asha | Math | 88 |
| Asha | Science | 91 |
| Ravi | Math | 78 |

Long-form data is often convenient for Seaborn because variables can be assigned to `x`, `y`, `hue`, `style`, and `size`.

**Wide-form data** can store separate groups in separate columns:

| Math | Science |
|---:|---:|
| 88 | 91 |
| 78 | 82 |

Seaborn supports both formats for many functions, but long-form data is generally more flexible for semantic mappings and faceting.

## Chapter 7 — Seaborn function families

Seaborn's plotting functions are commonly grouped into:
- Relational plots: relationships between variables.
- Distribution plots: shape and spread of data.
- Categorical plots: comparisons among categories.
- Regression plots: fitted statistical relationships.
- Matrix plots: heatmaps and clustered matrices.

Choose a function based on the question, not just its appearance.

---

# Part 2 — Relational plots

## Chapter 8 — Scatter plot

A scatter plot shows the relationship between two numerical variables.

```python
sns.scatterplot(data=df, x="study_hours", y="marks")
plt.show()
```

Useful parameters:
- `data`: DataFrame or compatible data source.
- `x`, `y`: columns or vectors to plot.
- `hue`: map a variable to color.
- `style`: map a variable to marker style.
- `size`: map a variable to marker size.
- `alpha`: transparency (supported by the underlying Matplotlib artist in relevant functions).

Example with multiple dimensions:
```python
sns.scatterplot(
    data=df,
    x="study_hours",
    y="marks",
    hue="course",
    style="course",
    size="attendance_percent"
)
```

A visible association does not prove that one variable causes the other.

## Chapter 9 — Line plot

Use line plots when the x-axis has a meaningful order, such as time or a sequence.

```python
sns.lineplot(data=df, x="month", y="revenue", hue="region")
```

By default, `lineplot` can estimate an aggregate and uncertainty interval when multiple observations share an x-value. If you want to draw the raw observations without aggregation, consider:
```python
sns.lineplot(data=df, x="time", y="value", estimator=None, errorbar=None)
```

For a simple single-series time trend, sort the data by time first.

## Chapter 10 — `relplot()` for relational grids

`relplot()` is a figure-level interface that can create scatter or line plots and supports faceting.

```python
sns.relplot(
    data=df,
    x="study_hours",
    y="marks",
    hue="course",
    col="classroom",
    kind="scatter"
)
```

Figure-level functions manage their own figure and axes. They are not passed an `ax=` argument in the same way as axes-level functions.

---

# Part 3 — Distribution plots

## Chapter 11 — Histogram with `histplot()`

A histogram groups numerical observations into bins.

```python
sns.histplot(data=df, x="salary", bins=15, kde=True)
plt.show()
```

Important options:
- `bins`: number or boundaries of bins.
- `kde=True`: overlay a kernel density estimate.
- `hue`: compare distributions by category.
- `stat`: choose count, frequency, probability, percent, or density behavior as supported by the installed version.

The choice of bin width can change the visible shape. Explain the binning choice when it matters.

## Chapter 12 — KDE plot

A kernel density estimate is a smoothed representation of a distribution.

```python
sns.kdeplot(data=df, x="salary", fill=True)
```

Compare groups:
```python
sns.kdeplot(data=df, x="salary", hue="department", common_norm=False)
```

KDE curves are estimates, not raw counts. Smoothing can hide small groups or unusual details.

## Chapter 13 — ECDF plot

An empirical cumulative distribution function shows the proportion of observations less than or equal to each value.

```python
sns.ecdfplot(data=df, x="response_time")
```

ECDF plots are useful for answering questions such as "What fraction of requests completed within 200 ms?"

## Chapter 14 — Rug plot

A rug plot marks individual observations along an axis.

```python
sns.rugplot(data=df, x="salary", height=0.05)
```

It can complement a histogram or KDE, but many observations can create visual clutter.

## Chapter 15 — `displot()` for distribution grids

`displot()` is a figure-level interface for histogram, KDE, and ECDF plots.

```python
sns.displot(
    data=df,
    x="salary",
    hue="department",
    col="location",
    kind="hist"
)
```

Use `displot()` when you want multiple panels or a figure-level distribution visualization.

## Chapter 16 — Comparing distributions

Useful choices:
- Histogram: frequency or density by bins.
- KDE: smoothed shape.
- ECDF: cumulative proportions.
- Box plot: median, quartiles, and potential outliers.
- Violin plot: distribution shape with summary information.

No single chart tells the entire story. Use complementary plots when needed.

---

# Part 4 — Categorical plots

## Chapter 17 — Bar plot

A bar plot estimates a statistic (mean by default in common usage) for each category and can show uncertainty.

```python
sns.barplot(data=df, x="department", y="salary", errorbar="ci")
```

A bar plot is not the same as a count plot. It summarizes a numerical variable by category.

## Chapter 18 — Count plot

A count plot shows how many observations belong to each category.

```python
sns.countplot(data=df, x="department")
```

Compare counts with hue:
```python
sns.countplot(data=df, x="department", hue="employment_type")
```

## Chapter 19 — Box plot

A box plot summarizes distributions across categories.

```python
sns.boxplot(data=df, x="department", y="salary")
```

It displays the median, quartiles, whiskers, and possible outliers according to the plotting convention.

## Chapter 20 — Violin plot

A violin plot combines a density shape with a categorical comparison.

```python
sns.violinplot(data=df, x="department", y="salary", inner="quart")
```

Use it when distribution shape matters. For small samples, density estimates can be unstable.

## Chapter 21 — Strip plot

A strip plot shows individual observations with categorical positioning.

```python
sns.stripplot(data=df, x="department", y="salary", jitter=True)
```

## Chapter 22 — Swarm plot

A swarm plot adjusts points to reduce overlap.

```python
sns.swarmplot(data=df, x="department", y="salary")
```

Swarm plots can become slow or crowded with large datasets. Consider sampling or using a box/violin plot with a transparent strip overlay.

## Chapter 23 — Combining categorical plots

A common teaching pattern is to show a summary and the raw observations together.

```python
fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(data=df, x="department", y="salary", ax=ax, color="lightgray")
sns.stripplot(data=df, x="department", y="salary", ax=ax,
              color="black", alpha=0.45, jitter=True)
plt.show()
```

---

# Part 5 — Regression plots

## Chapter 24 — Regression plot with `regplot()`

`regplot()` draws a scatter plot and fits a regression model.

```python
sns.regplot(data=df, x="study_hours", y="marks")
```

The shaded region commonly represents an estimated confidence interval for the regression fit.

## Chapter 25 — `lmplot()` for regression grids

`lmplot()` is a figure-level regression interface with faceting.

```python
sns.lmplot(
    data=df,
    x="study_hours",
    y="marks",
    hue="course",
    col="classroom"
)
```

## Chapter 26 — Residual plot

Residuals are the differences between observed and model-predicted values.

```python
sns.residplot(data=df, x="study_hours", y="marks")
```

Residual plots can help inspect patterns not captured by a simple fitted relationship. They do not replace formal model diagnostics.

---

# Part 6 — Multi-variable analysis and grids

## Chapter 27 — The `hue`, `style`, and `size` semantics

These parameters encode additional variables:
- `hue`: color.
- `style`: marker or line style.
- `size`: marker or line size.

```python
sns.scatterplot(
    data=df,
    x="experience_years",
    y="salary",
    hue="department",
    style="employment_type",
    size="performance_score"
)
```

Avoid encoding too many variables at once. A chart can become difficult to decode.

## Chapter 28 — Faceting with `FacetGrid`

Faceting creates a separate panel for each category or category combination.

```python
g = sns.FacetGrid(df, col="department", hue="employment_type")
g.map_dataframe(sns.scatterplot, x="experience_years", y="salary")
g.add_legend()
```

## Chapter 29 — Pair plot

A pair plot compares pairwise relationships among several numerical variables.

```python
sns.pairplot(
    df,
    vars=["study_hours", "attendance_percent", "marks"],
    hue="course"
)
```

Pair plots can become large. Select a small set of meaningful variables.

## Chapter 30 — PairGrid

`PairGrid` provides more control over the plot type used in each region.

```python
g = sns.PairGrid(df, vars=["study_hours", "attendance_percent", "marks"])
g.map_diag(sns.histplot)
g.map_offdiag(sns.scatterplot)
```

## Chapter 31 — Joint plot

A joint plot shows a relationship plus the marginal distributions of each variable.

```python
sns.jointplot(data=df, x="study_hours", y="marks", kind="reg")
```

Other useful kinds include scatter, KDE, and histogram modes supported by the installed Seaborn version.

## Chapter 32 — JointGrid

`JointGrid` is the lower-level interface when you need custom joint and marginal plots.

```python
g = sns.JointGrid(data=df, x="study_hours", y="marks")
g.plot_joint(sns.scatterplot)
g.plot_marginals(sns.histplot)
```

---

# Part 7 — Matrix plots

## Chapter 33 — Correlation matrix

Correlation measures the strength and direction of a linear relationship between numerical variables when using Pearson correlation.

```python
numeric_df = df.select_dtypes(include="number")
correlation = numeric_df.corr()
print(correlation)
```

Correlation does not prove causation and can be affected by outliers, non-linear relationships, and confounding variables.

## Chapter 34 — Heatmap

```python
sns.heatmap(correlation, annot=True, cmap="coolwarm", center=0)
plt.show()
```

Useful options:
- `annot=True`: show values in cells.
- `cmap`: color map.
- `center=0`: center the color scale at zero.
- `vmin`, `vmax`: control the scale.
- `linewidths`: draw separators between cells.

## Chapter 35 — Cluster map

A clustermap groups rows and columns based on similarity.

```python
sns.clustermap(correlation, cmap="vlag", center=0, annot=True)
```

Clustering is meaningful only when the selected distance and linkage choices make sense for the data. It can be computationally expensive for large matrices.

---

# Part 8 — Themes and customization

## Chapter 36 — Seaborn themes

Set a global theme:
```python
sns.set_theme(style="whitegrid", context="notebook")
```

Common styles include:
- `darkgrid`
- `whitegrid`
- `dark`
- `white`
- `ticks`

Context presets include:
- `paper`
- `notebook`
- `talk`
- `poster`

## Chapter 37 — Color palettes

Inspect palettes:
```python
sns.color_palette("deep")
sns.color_palette("muted")
sns.color_palette("Set2")
```

Apply a palette:
```python
sns.set_palette("Set2")
```

Use qualitative palettes for categories and sequential/diverging palettes for ordered numerical values. Consider color-vision accessibility.

## Chapter 38 — Axes and figure customization

```python
fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(data=df, x="department", y="salary", ax=ax)
ax.set_title("Salary Distribution by Department")
ax.set_xlabel("Department")
ax.set_ylabel("Annual salary")
ax.tick_params(axis="x", rotation=25)
fig.tight_layout()
```

## Chapter 39 — Legends

Seaborn usually creates legends automatically when a semantic variable is used.

Matplotlib can customize the legend:
```python
ax.legend(title="Department", loc="best", frameon=True)
```

If the chart does not need a legend, remove it intentionally rather than leaving confusing labels.

## Chapter 40 — Saving figures

For axes-level plots:
```python
fig, ax = plt.subplots()
sns.histplot(data=df, x="salary", ax=ax)
fig.savefig("salary_distribution.png", dpi=300, bbox_inches="tight")
```

For figure-level plots:
```python
g = sns.displot(data=df, x="salary")
g.savefig("salary_distribution.png", dpi=300, bbox_inches="tight")
```

Common formats:
- PNG for web and slides.
- SVG for scalable vector graphics.
- PDF for reports and printing.

---

# Part 9 — Working with real datasets

## Chapter 41 — Loading CSV files

```python
import pandas as pd
df = pd.read_csv("data/input/employees.csv")
```

Inspect:
```python
print(df.head())
print(df.shape)
print(df.info())
print(df.describe(include="all"))
print(df.isna().sum())
```

## Chapter 42 — Data cleaning before plotting

Examples:
```python
df = df.drop_duplicates()
df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
df = df.dropna(subset=["salary", "department"])
```

Do not remove missing values automatically without understanding why they are missing and how that affects the analysis.

## Chapter 43 — Filtering and sorting

```python
engineering = df[df["department"] == "Engineering"]
top_salaries = df.sort_values("salary", ascending=False).head(10)
```

Filter first when the full dataset would make the visualization too dense.

## Chapter 44 — Aggregation with Pandas

```python
summary = df.groupby("department", as_index=False).agg(
    average_salary=("salary", "mean"),
    employee_count=("employee_id", "count")
)
```

Use Seaborn to visualize the resulting summary or pass the original data when Seaborn's estimator is appropriate. Be clear about whether the chart shows raw records or aggregated values.

## Chapter 45 — Dates and time series

```python
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")
sns.lineplot(data=df, x="date", y="value", hue="service")
plt.xticks(rotation=30)
```

For repeated measurements at the same timestamp, understand Seaborn's aggregation and uncertainty behavior before interpreting the line.

---

# Part 10 — Best practices and troubleshooting

## Chapter 46 — Choosing the right chart

| Question | Suggested chart |
|---|---|
| How do two numerical variables relate? | Scatter plot |
| How does a metric change over time? | Line plot |
| How many observations are in each category? | Count plot |
| How does a numerical metric differ by category? | Box, violin, or bar plot |
| What is the shape of a numerical distribution? | Histogram, KDE, or ECDF |
| How are many numerical variables related? | Pair plot or correlation heatmap |
| How do patterns differ across groups? | Faceted plot |

## Chapter 47 — Common mistakes

1. Using `barplot()` when the question asks for counts; use `countplot()` for counts.
2. Forgetting that `barplot()` summarizes a numerical variable by category.
3. Using unsorted dates in a line chart.
4. Treating correlation as proof of causation.
5. Using a KDE plot for a tiny sample without caution.
6. Adding too many hue categories and making the legend unreadable.
7. Creating a huge pair plot with too many variables.
8. Forgetting to pass `ax=` when placing an axes-level plot in a subplot.
9. Calling `plt.savefig()` after the wrong figure has become active; prefer `fig.savefig()`.
10. Not checking missing values and data types before plotting.
11. Comparing groups with very different sample sizes without noting the imbalance.
12. Assuming every Seaborn function returns the same type of object.

## Chapter 48 — Axes-level versus figure-level functions

**Axes-level functions** draw into one Matplotlib Axes and generally accept `ax=`:
- `scatterplot`
- `lineplot`
- `histplot`
- `kdeplot`
- `boxplot`
- `violinplot`
- `barplot`
- `countplot`
- `heatmap`
- `regplot`

**Figure-level functions** manage a complete figure and may create grids:
- `relplot`
- `displot`
- `catplot`
- `lmplot`
- `pairplot`
- `jointplot`
- `clustermap`

Figure-level functions return grid objects. For example, a `relplot()` result has a `.figure` property and can be saved with its `.savefig()` method.

## Chapter 49 — Final EDA checklist

Before presenting findings:
- Is the question clearly stated?
- Are data types and missing values checked?
- Is the chart type appropriate?
- Are axes and units labeled?
- Are groups and sample sizes clear?
- Is the legend readable?
- Are outliers represented honestly?
- Are uncertainty intervals interpreted correctly?
- Are findings described without claiming unsupported causation?
- Can someone reproduce the chart from the script and source data?

---

# Part 11 — Practical Projects

## Project 1 — Employee Analytics and Salary EDA

**Goal:** Explore salary, experience, performance, and department patterns.

Folder: `project_01_employee_analytics/`

Run from the repository root:
```bash
python project_01_employee_analytics/main.py
```

The project:
- Loads employee data with Pandas.
- Checks and prepares columns.
- Creates a salary distribution histogram.
- Compares salary distributions by department.
- Plots experience versus salary with a regression line.
- Creates a correlation heatmap.
- Saves a department summary CSV and chart images.

Expected outputs:
- `salary_distribution.png`
- `salary_by_department.png`
- `experience_vs_salary.png`
- `correlation_heatmap.png`
- `department_summary.csv`

Teaching questions:
1. Which department has the highest median salary?
2. Does salary appear to increase with experience?
3. Which numerical variables have the strongest correlation?
4. Why might a box plot be more informative than a bar plot for salary comparisons?
5. Does the observed relationship prove experience causes higher salary?

## Project 2 — Student Performance EDA

**Goal:** Explore how study hours, attendance, assignments, sleep, and course relate to student marks.

Folder: `project_02_student_performance/`

Run:
```bash
python project_02_student_performance/main.py
```

The project:
- Loads student performance records.
- Creates a study-hours versus marks scatter plot.
- Adds course as a hue variable.
- Compares marks distributions by course.
- Creates a pair plot for numerical variables.
- Generates a correlation heatmap.
- Saves a course-level summary CSV.

Expected outputs:
- `study_hours_vs_marks.png`
- `marks_by_course.png`
- `student_pairplot.png`
- `student_correlation_heatmap.png`
- `course_summary.csv`

Teaching questions:
1. Which course has the highest average marks?
2. Does attendance appear related to marks?
3. Are there unusual observations?
4. What extra information does hue add to the scatter plot?
5. Why should correlation not be interpreted as causation?

---

# Part 12 — Practice and assessment

## Beginner exercises
1. Load a CSV using Pandas and show its first five rows.
2. Create a scatter plot for two numerical columns.
3. Create a histogram for one numerical column.
4. Create a count plot for a categorical column.
5. Add a title, axis labels, and a theme.

## Intermediate exercises
1. Compare a numerical variable across categories using a box plot.
2. Add `hue` to a scatter plot.
3. Create a line plot for a time-series dataset.
4. Create a heatmap from a correlation matrix.
5. Use `FacetGrid` to create separate panels.
6. Combine a box plot and strip plot.
7. Save charts as PNG and PDF.

## Advanced exercises
1. Create a `PairGrid` with histograms on the diagonal and scatter plots elsewhere.
2. Build a faceted regression analysis.
3. Compare ECDF and KDE representations of the same distribution.
4. Create a dashboard with four Axes-level plots.
5. Investigate how outliers affect a correlation heatmap.
6. Create a report with clear chart captions and caveats.

## Suggested teaching sequence

| Session | Topics | Practical |
|---|---|---|
| 1 | Seaborn setup, DataFrame plotting, themes | First scatter plot |
| 2 | Relational plots, hue, style, size | Multi-variable scatter |
| 3 | Histograms, KDE, ECDF | Distribution comparison |
| 4 | Categorical plots | Department comparison |
| 5 | Regression plots and grids | Relationship analysis |
| 6 | Pair plots, joint plots, heatmaps | Multi-variable EDA |
| 7 | Project 1 | Employee analytics |
| 8 | Project 2 | Student performance |

---

# Repository structure

```text
Python_Seaborn_Toolkit/
├── README.md
├── requirements.txt
├── project_01_employee_analytics/
│   ├── README.md
│   ├── main.py
│   ├── data/
│   │   ├── input/employees.csv
│   │   └── reference/departments.csv
│   ├── output/
│   └── logs/
└── project_02_student_performance/
    ├── README.md
    ├── main.py
    ├── data/
    │   ├── input/students.csv
    │   └── reference/courses.csv
    ├── output/
    └── logs/
```

## Run both projects

From the repository root:
```bash
pip install -r requirements.txt
python project_01_employee_analytics/main.py
python project_02_student_performance/main.py
```

Both scripts resolve input and output paths relative to their own file location, so they do not depend on the terminal's current working directory.
