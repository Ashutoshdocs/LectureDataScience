# Matplotlib: Complete Beginner-to-Advanced Teaching Guide

A practical course for learning **Matplotlib** from the first plot through publication-quality visualizations. It includes two runnable projects, sample datasets, and exercises.

## Learning outcomes

By the end, students should be able to:
- Explain what Matplotlib is and when visualization is useful.
- Create and customize line, bar, scatter, histogram, pie, box, area, and time-series charts.
- Understand the `Figure` and `Axes` object model.
- Add titles, labels, legends, annotations, grids, ticks, and reference lines.
- Work with multiple plots, shared axes, twin axes, and subplot layouts.
- Style charts, use colors responsibly, and improve readability.
- Save charts in PNG, JPG, SVG, and PDF formats.
- Visualize data from NumPy arrays and Pandas DataFrames.
- Build reusable plotting functions and create dashboard-style reports.

---

# Part 1 — Foundations

## Chapter 1 — What is data visualization?

Data visualization represents information graphically so people can identify patterns, comparisons, trends, relationships, and unusual values.

Examples:
- A line chart can show how monthly sales change.
- A bar chart can compare sales across regions.
- A histogram can show the distribution of employee salaries.
- A scatter plot can show whether study hours are related to marks.

A chart should answer a question. Do not add visual effects that make the answer harder to understand.

## Chapter 2 — What is Matplotlib?

Matplotlib is a Python plotting library. Its main plotting interface is `matplotlib.pyplot`, commonly imported as `plt`.

It is useful for:
- Exploratory data analysis.
- Scientific and engineering plots.
- Business reports.
- Statistical charts.
- Exporting static charts for documents and presentations.

Matplotlib is not the same as Pandas or NumPy:
- NumPy provides numerical arrays and calculations.
- Pandas organizes and analyzes tabular data.
- Matplotlib turns data into visual charts.

## Chapter 3 — Environment setup

Create a project folder and virtual environment.

### Windows PowerShell
```powershell
mkdir matplotlib-course
cd matplotlib-course
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install matplotlib numpy pandas
```

### Linux / macOS
```bash
mkdir matplotlib-course
cd matplotlib-course
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install matplotlib numpy pandas
```

Verify:
```bash
python -c "import matplotlib; print(matplotlib.__version__)"
```

Install from this repository:
```bash
pip install -r requirements.txt
```

## Chapter 4 — Your first chart

```python
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr"]
sales = [120, 150, 135, 190]

plt.plot(months, sales)
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.show()
```

Important functions:
- `plt.plot()` creates a line plot.
- `plt.title()` sets the chart title.
- `plt.xlabel()` labels the horizontal axis.
- `plt.ylabel()` labels the vertical axis.
- `plt.show()` displays the chart.

## Chapter 5 — Figure and Axes: the object-oriented model

Matplotlib has two important objects:
- **Figure**: the complete canvas or window.
- **Axes**: an individual plotting area inside the Figure. A Figure can contain multiple Axes.

Recommended pattern for reusable and multi-chart work:

```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4]
y = [2, 5, 4, 8]

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(x, y, marker="o", label="Observed")
ax.set_title("Example")
ax.set_xlabel("X value")
ax.set_ylabel("Y value")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
plt.show()
```

Use `ax.plot()` and `ax.set_title()` when working with an Axes object. This makes it easier to manage multiple charts.

## Chapter 6 — Line charts

Use line charts when the order of x-values matters, especially for time trends.

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [10, 14, 13, 20],
        color="steelblue", marker="o", linestyle="-",
        linewidth=2, markersize=6, label="Actual")
ax.legend()
plt.show()
```

Common options:
- `color`: line color.
- `marker`: point marker such as `"o"`, `"s"`, `"^"`.
- `linestyle`: `"-"`, `"--"`, `":"`, `"-."`.
- `linewidth`: line thickness.
- `markersize`: marker size.
- `label`: legend entry.

Plot multiple series:
```python
fig, ax = plt.subplots()
ax.plot(months, actual, label="Actual")
ax.plot(months, target, label="Target", linestyle="--")
ax.legend()
```

## Chapter 7 — Bar charts

Use bars to compare categories.

```python
departments = ["IT", "HR", "Sales", "Finance"]
employees = [42, 12, 35, 18]

fig, ax = plt.subplots()
bars = ax.bar(departments, employees)
ax.bar_label(bars, padding=3)
ax.set_title("Employees by Department")
ax.set_ylabel("Employee count")
plt.show()
```

Horizontal bars:
```python
ax.barh(departments, employees)
```

Grouped bars:
```python
import numpy as np

x = np.arange(len(departments))
width = 0.35
fig, ax = plt.subplots()
ax.bar(x - width/2, current, width, label="Current")
ax.bar(x + width/2, previous, width, label="Previous")
ax.set_xticks(x, departments)
ax.legend()
```

Stacked bars use the `bottom=` argument to place one series on top of another.

## Chapter 8 — Scatter plots

Use scatter plots to explore relationships between two numerical variables.

```python
study_hours = [1, 2, 3, 4, 5]
marks = [42, 50, 61, 72, 85]

fig, ax = plt.subplots()
ax.scatter(study_hours, marks, s=70, alpha=0.75)
ax.set_xlabel("Study hours")
ax.set_ylabel("Marks")
plt.show()
```

Useful parameters:
- `s`: marker area.
- `alpha`: transparency.
- `c`: color or numeric values mapped to colors.
- `marker`: marker shape.

A visible relationship does not automatically prove causation.

## Chapter 9 — Histograms

A histogram shows the distribution of a numerical variable by grouping values into bins.

```python
scores = [45, 52, 58, 61, 62, 67, 71, 73, 74, 80, 85, 91]

fig, ax = plt.subplots()
ax.hist(scores, bins=5, edgecolor="black")
ax.set_xlabel("Score")
ax.set_ylabel("Frequency")
plt.show()
```

`bins` controls the number or boundaries of intervals. Too few bins can hide structure; too many can make the chart noisy.

## Chapter 10 — Pie charts

Pie charts show parts of a whole. Use only when categories are few and values form a meaningful whole.

```python
labels = ["Cloud", "On-premises", "Hybrid"]
values = [50, 20, 30]

fig, ax = plt.subplots()
ax.pie(values, labels=labels, autopct="%1.1f%%",
       startangle=90)
ax.set_title("Infrastructure Distribution")
ax.axis("equal")
plt.show()
```

For precise comparisons across many categories, a bar chart is usually easier to read.

## Chapter 11 — Box plots

Box plots summarize a distribution:
- Median: line inside the box.
- Lower and upper quartiles: box boundaries.
- Whiskers: range determined by the plotting rule.
- Fliers: points beyond the whiskers.

```python
fig, ax = plt.subplots()
ax.boxplot([team_a, team_b], tick_labels=["Team A", "Team B"])
ax.set_ylabel("Resolution time (hours)")
plt.show()
```

## Chapter 12 — Area and step charts

Area chart:
```python
ax.fill_between(days, minimum, maximum, alpha=0.25,
                label="Expected range")
ax.plot(days, actual, label="Actual")
ax.legend()
```

Stacked area:
```python
ax.stackplot(months, product_a, product_b, product_c,
             labels=["A", "B", "C"])
ax.legend(loc="upper left")
```

Step chart:
```python
ax.step(time_points, state_values, where="post")
```

## Chapter 13 — Titles, labels, legends, and grids

```python
fig, ax = plt.subplots()
ax.plot(x, y, label="Latency")
ax.set_title("API Latency by Hour", fontsize=14, fontweight="bold")
ax.set_xlabel("Hour")
ax.set_ylabel("Latency (ms)")
ax.legend(loc="best")
ax.grid(axis="y", linestyle="--", alpha=0.35)
```

Use units in axis labels. A label such as `Latency (ms)` is more informative than `Latency`.

## Chapter 14 — Ticks and axis limits

```python
ax.set_xlim(0, 12)
ax.set_ylim(0, 100)
ax.set_xticks([0, 3, 6, 9, 12])
ax.tick_params(axis="x", rotation=30)
```

Avoid truncating axes in ways that exaggerate differences, especially for bar charts.

## Chapter 15 — Annotations and reference lines

```python
ax.axhline(80, color="red", linestyle="--", label="SLO threshold")
ax.annotate("Peak", xy=(peak_x, peak_y),
            xytext=(peak_x + 1, peak_y + 10),
            arrowprops={"arrowstyle": "->"})
```

Other useful helpers:
- `ax.axvline()` vertical reference line.
- `ax.axhspan()` horizontal shaded band.
- `ax.text()` place text at data coordinates.

## Chapter 16 — Colors and styles

Matplotlib supports named colors, hex values, RGB tuples, colormaps, and style sheets.

```python
plt.style.use("ggplot")
```

List available styles:
```python
print(plt.style.available)
```

Use color to encode meaning consistently. Ensure text and plotted elements have sufficient contrast. Do not rely on color alone to communicate a critical distinction.

## Chapter 17 — Figure size and resolution

```python
fig, ax = plt.subplots(figsize=(10, 5), dpi=120)
```

- `figsize` is measured in inches.
- `dpi` means dots per inch.
- Larger DPI can improve raster output sharpness but also increases file size.

## Chapter 18 — Multiple subplots

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
axes[0, 0].plot(x, y)
axes[0, 0].set_title("Line")
axes[0, 1].bar(categories, values)
axes[0, 1].set_title("Bar")
axes[1, 0].scatter(x, y)
axes[1, 0].set_title("Scatter")
axes[1, 1].hist(values)
axes[1, 1].set_title("Histogram")
fig.tight_layout()
```

`axes` is an array of Axes objects. Index it by row and column.

For a single row:
```python
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
```

For shared axes:
```python
fig, axes = plt.subplots(2, 1, sharex=True)
```

## Chapter 19 — Layout management

Use:
```python
fig.tight_layout()
```

Or:
```python
fig, axes = plt.subplots(2, 2, constrained_layout=True)
```

Do not normally combine multiple layout engines without understanding their interaction.

## Chapter 20 — Saving charts

```python
fig.savefig("sales_chart.png", dpi=300, bbox_inches="tight")
fig.savefig("sales_chart.svg", bbox_inches="tight")
fig.savefig("sales_chart.pdf", bbox_inches="tight")
```

Formats:
- PNG: common for web and slides.
- JPG: photographic/raster output; usually not ideal for line art.
- SVG: scalable vector output.
- PDF: convenient for reports and printing.

Save before `plt.show()` in scripts to avoid backend-dependent surprises.

## Chapter 21 — NumPy integration

```python
import numpy as np
x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
```

NumPy is useful for generating numerical sequences and mathematical functions.

## Chapter 22 — Pandas integration

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales.csv")
fig, ax = plt.subplots()
ax.plot(df["month"], df["sales"])
ax.set_xlabel("Month")
ax.set_ylabel("Sales")
plt.show()
```

Pandas also provides quick plotting:
```python
df.plot(x="month", y="sales", kind="line")
```

Pandas plotting uses Matplotlib by default. For more control, use Matplotlib's Axes methods directly.

## Chapter 23 — Date and time axes

Convert date strings into datetime values:
```python
import pandas as pd
dates = pd.to_datetime(["2026-01-01", "2026-02-01", "2026-03-01"])
ax.plot(dates, values)
fig.autofmt_xdate()
```

For dense time-series labels, format dates and rotate labels carefully.

## Chapter 24 — Twin axes

Use a second y-axis only when it genuinely helps compare variables with different units.

```python
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(days, temperature, color="tab:red")
ax2.plot(days, energy_use, color="tab:blue")
ax1.set_ylabel("Temperature (°C)")
ax2.set_ylabel("Energy (kWh)")
```

Twin axes can mislead because the scales are independent. Label both axes clearly.

## Chapter 25 — Logarithmic scales

Useful when values span several orders of magnitude.

```python
ax.set_yscale("log")
```

A logarithmic scale cannot display zero or negative values in the usual way. Explain the scale to the reader.

## Chapter 26 — Error bars

```python
ax.errorbar(x, averages, yerr=standard_errors,
            fmt="o-", capsize=4)
```

Error bars can represent standard deviation, standard error, confidence intervals, or measurement uncertainty. State which one is being shown.

## Chapter 27 — Heatmaps with imshow

```python
import numpy as np
matrix = np.array([[10, 20, 30], [15, 25, 35]])

fig, ax = plt.subplots()
image = ax.imshow(matrix, aspect="auto")
fig.colorbar(image, ax=ax, label="Value")
ax.set_xticks(range(3), ["A", "B", "C"])
ax.set_yticks(range(2), ["North", "South"])
plt.show()
```

## Chapter 28 — Images and color maps

`imshow()` displays a 2D array or image. Colormaps map numerical values to colors.

```python
image = ax.imshow(matrix, cmap="viridis")
fig.colorbar(image, ax=ax)
```

Choose sequential colormaps for ordered magnitude, diverging maps for values around a meaningful center, and qualitative palettes for categories.

## Chapter 29 — Reusable plotting functions

```python
def plot_metric(ax, x_values, y_values, title, y_label):
    ax.plot(x_values, y_values, marker="o")
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel(y_label)
    ax.grid(True, alpha=0.25)
```

Reusable functions reduce repeated formatting and help keep charts consistent.

## Chapter 30 — Object-oriented versus pyplot interface

Pyplot is convenient for quick interactive plots:
```python
plt.plot(x, y)
plt.title("Quick chart")
```

Object-oriented Matplotlib is recommended for scripts and multiple plots:
```python
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("Reusable chart")
```

The two interfaces can coexist, but avoid mixing them unnecessarily in complex code.

## Chapter 31 — Backends and environments

A backend controls how Matplotlib renders charts:
- Interactive backends display windows and support interaction.
- Non-interactive backends render files, such as in automated jobs.

In notebooks, charts often display inline. On servers without a display, save figures to files instead of expecting a GUI window.

Do not change the backend after importing `pyplot` unless you understand the environment requirements.

## Chapter 32 — Common mistakes and troubleshooting

1. **Blank chart**: check that the correct Axes received the plotting call.
2. **No chart window**: check the environment/backend; save to a file.
3. **Labels overlap**: use `fig.tight_layout()`, rotate labels, or increase figure size.
4. **Legend missing**: supply `label=` and call `ax.legend()`.
5. **Wrong chart type**: select a chart based on the question and data type.
6. **Unexpected line order**: sort time-series data by date before plotting.
7. **Too many categories**: use a sorted horizontal bar chart or filter the view.
8. **Figures accumulate in loops**: close figures after saving with `plt.close(fig)`.
9. **Output path not found**: create the parent directory before saving.
10. **Misleading axes**: label units and choose limits carefully.

## Chapter 33 — A professional chart checklist

Before sharing a chart, ask:
- Does the title explain what is being shown?
- Are both axes labeled with units?
- Is the chart type appropriate?
- Are categories ordered logically?
- Is the legend necessary and understandable?
- Are labels readable at the final size?
- Does the scale tell the truth?
- Is the source or time period stated when needed?
- Is the chart saved in a suitable format?

---

# Part 2 — Practical Projects

## Project 1 — Business Sales Visualization Report

**Goal:** Analyze a sample monthly sales dataset and create a set of charts for a business review.

Folder: `project_01_sales_visualization/`

Run:
```bash
python project_01_sales_visualization/main.py
```

The project:
- Loads CSV data with Pandas.
- Calculates revenue from units and unit price.
- Aggregates sales by month, region, and product.
- Creates line, bar, and pie charts.
- Saves charts in `output/`.
- Saves a summary CSV.

Expected output files:
- `monthly_revenue.png`
- `revenue_by_region.png`
- `revenue_by_product.png`
- `sales_summary.csv`

Teaching questions:
1. Which month has the highest revenue?
2. Which region contributes most?
3. Which product has the highest revenue?
4. Would a pie chart or bar chart be clearer for comparing regions? Why?
5. Change the chart title and add data labels.

## Project 2 — Infrastructure Monitoring Dashboard

**Goal:** Visualize CPU, memory, disk utilization, and response latency from sample monitoring data.

Folder: `project_02_infrastructure_dashboard/`

Run:
```bash
python project_02_infrastructure_dashboard/main.py
```

The project:
- Loads time-series monitoring data.
- Parses timestamps.
- Creates a multi-panel dashboard.
- Adds an 80% utilization threshold.
- Highlights latency and resource trends.
- Exports a high-resolution PNG and PDF.

Expected output files:
- `infrastructure_dashboard.png`
- `infrastructure_dashboard.pdf`
- `daily_summary.csv`

Teaching questions:
1. Which server has the highest average CPU?
2. When does memory utilization peak?
3. How many samples exceed the CPU threshold?
4. Why is a line chart appropriate for monitoring metrics?
5. Add a threshold line for memory and disk.

---

# Part 3 — Practice and Assessment

## Beginner exercises
1. Plot five student marks using a line chart.
2. Compare marks by subject using a bar chart.
3. Create a histogram of 30 random values.
4. Add title, axis labels, and a legend.
5. Save a chart as PNG.

## Intermediate exercises
1. Create a 2×2 subplot layout.
2. Plot two monthly sales series on the same Axes.
3. Add a horizontal target line.
4. Create a scatter plot with marker size and transparency.
5. Read a CSV with Pandas and plot a selected column.
6. Format a date axis.
7. Add annotations to the highest data point.

## Advanced exercises
1. Create a reusable chart function accepting an Axes object.
2. Build a dashboard with four related metrics.
3. Use a heatmap to display a matrix.
4. Add error bars to experimental measurements.
5. Export the same figure to PNG, SVG, and PDF.
6. Compare a linear and logarithmic y-axis.
7. Build a monitoring report that identifies threshold breaches.

## Final assessment project

Create a visualization report for a dataset of your choice:
- State the business or scientific question.
- Clean and prepare the data.
- Choose at least four suitable chart types.
- Explain what each chart reveals.
- Use consistent titles, labels, units, and styles.
- Save charts in an `output/` folder.
- Write a short conclusion based on the evidence.

## Suggested teaching sequence

| Session | Topics | Practical |
|---|---|---|
| 1 | Visualization concepts, setup, first plot | Line chart |
| 2 | Figure, Axes, labels, legends, styles | Customized line chart |
| 3 | Bar, scatter, histogram, pie | Comparison charts |
| 4 | Box, area, annotations, reference lines | Statistical charts |
| 5 | Subplots, layout, savefig | Multi-chart report |
| 6 | NumPy, Pandas, dates, heatmaps | Data-driven plotting |
| 7 | Project 1 | Sales report |
| 8 | Project 2 | Infrastructure dashboard |

---

# Repository structure

```text
Python_Matplotlib_Toolkit/
├── README.md
├── requirements.txt
├── project_01_sales_visualization/
│   ├── README.md
│   ├── main.py
│   ├── data/
│   │   ├── input/
│   │   │   └── sales.csv
│   │   └── reference/
│   │       └── regions.csv
│   ├── output/
│   └── logs/
└── project_02_infrastructure_dashboard/
    ├── README.md
    ├── main.py
    ├── data/
    │   ├── input/
    │   │   └── infrastructure_metrics.csv
    │   └── reference/
    │       └── thresholds.csv
    ├── output/
    └── logs/
```

## Run both projects

From the repository root:
```bash
pip install -r requirements.txt
python project_01_sales_visualization/main.py
python project_02_infrastructure_dashboard/main.py
```

Each script resolves its own data and output directories relative to its file location, so it does not depend on the terminal's current working directory.
