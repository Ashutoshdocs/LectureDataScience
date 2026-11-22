# Data Visualization Demo – Matplotlib & Seaborn

A hands-on demo project that follows the course outline topic by topic.
**One common file** (`common.py`) provides the data and helpers, and **each topic has its own Python file**.

---

## 📁 Project Structure

```
data_viz_demo/
├── common.py                          # Shared: datasets, style, save helper
├── 01_intro_data_visualization.py     # Why visualize? Table vs chart
├── 02_line_plots_matplotlib.py        # Plotting Charts using Matplotlib
├── 03_bar_charts.py                   # Bar Charts
├── 04_pie_charts.py                   # Pie Charts
├── 05_stack_plots.py                  # Stack Plots
├── 06_histograms.py                   # Histograms
├── 07_scatter_plots.py                # Scatter Plots
├── 08_subplots.py                     # Subplots
├── 09_intro_seaborn.py                # Introduction to Seaborn
├── 10_basic_plot_types_seaborn.py     # Basic Plot Types in Seaborn
├── run_all.py                         # Runs every demo, saves all charts
├── requirements.txt
└── output/                            # Charts are saved here (auto-created)
```

---

## ⚙️ How to Run

```bash
# 1. (Optional) create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 2. Install libraries
pip install -r requirements.txt

# 3. Run any single topic (a chart window opens + PNG saved to output/)
python 03_bar_charts.py

# 4. Or run everything at once (no windows, just saves PNGs)
python run_all.py
```

> Close each chart window to continue to the next chart in the same script.

---

## 🔗 The Common File – `common.py`

Every topic script starts with `from common import ...`. This avoids repeating the same setup code in 10 files.

| Function | What it gives you |
|---|---|
| `apply_style()` | One consistent look (grid, font sizes, figure size) |
| `get_monthly_sales()` | 12 months × 3 categories (Electronics, Clothing, Groceries) |
| `get_students(n=200)` | study_hours, sleep_hours, score, gender, grade_level |
| `get_market_share()` | Brand → % dictionary (parts of a whole) |
| `save_and_show(fig, name)` | Saves PNG to `output/` and shows the window |

Data is generated with a fixed random seed, so you get the **same numbers every run** and **no internet or CSV is needed**.

---

## 📚 Topics Explained

### 1. Introduction to Data Visualization — `01_intro_data_visualization.py`
**What:** Turning numbers into pictures so patterns, trends and outliers become obvious.
**Why:** The human eye spots a rising line instantly but struggles with a table of 36 numbers.
**How the demo works:** prints the raw sales table, then plots the same data as a line chart.
**Key idea:** every good chart has a **title, axis labels, and a legend**.

**Choosing a chart:**
| Goal | Chart |
|---|---|
| Trend over time | Line |
| Compare categories | Bar |
| Parts of a whole | Pie / Stack plot |
| Distribution of one variable | Histogram |
| Relationship between two variables | Scatter |

---

### 2. Plotting Charts using Matplotlib — `02_line_plots_matplotlib.py`
**What:** Matplotlib is Python's core plotting library. `plt.plot()` draws line charts.
**Two ways to write code:**
```python
# pyplot style (quick)
plt.plot(x, y); plt.title("..."); plt.show()

# Object-Oriented style (recommended)
fig, ax = plt.subplots()
ax.plot(x, y); ax.set_title("...")
```
**Covers:** `color`, `linestyle` (`-`, `--`, `:`), `marker` (`o`, `s`, `^`), `linewidth`, `label` + `legend()`, `set_ylim()`, and `annotate()` to point at the peak.

---

### 3. Bar Charts — `03_bar_charts.py`
**What:** Rectangles whose length represents a value — best for comparing categories.
**How:**
- `ax.bar(x, height)` → vertical bars
- `ax.barh(y, width)` → horizontal bars (good for long labels)
- Grouped bars → shift each series by `width` using `np.arange()` positions
- `ax.bar_label(bars)` → prints the value on each bar

---

### 4. Pie Charts — `04_pie_charts.py`
**What:** A circle split into slices showing each part's share of 100%.
**How:** `ax.pie(sizes, labels=..., autopct="%1.1f%%")`
- `explode` → pull a slice out to highlight it
- `startangle=90` → start from the top
- `wedgeprops={"width": 0.4}` → turns it into a **donut chart**
- `ax.axis("equal")` → keeps it a perfect circle

**Tip:** use pies only for a few categories (≤ 5–6); otherwise use a bar chart.

---

### 5. Stack Plots — `05_stack_plots.py`
**What:** Stacked area chart — each band is one category; the top edge is the total.
**How:** `ax.stackplot(x, y1, y2, y3, labels=[...])`
**Demo shows two versions:**
1. Absolute values → how the **total** grows and what it's made of
2. 100% stack → how each category's **share** changes (divide each row by its total)

---

### 6. Histograms — `06_histograms.py`
**What:** Splits numeric data into ranges (**bins**) and counts values in each — shows the *shape* of a distribution.
**How:** `ax.hist(data, bins=15, edgecolor="white")`
**Demo shows:**
- A mean line with `ax.axvline()`
- Effect of bins: 5 (too coarse) vs 15 (good) vs 50 (too noisy)
- Overlapping histograms with `alpha` to compare Male vs Female

**Bar vs Histogram:** bar = categories, histogram = continuous numbers.

---

### 7. Scatter Plots — `07_scatter_plots.py`
**What:** One dot per record, x vs y — shows **relationships / correlation**.
**How:** `ax.scatter(x, y)`
- `np.polyfit(x, y, 1)` → draw a best-fit trend line
- `df.corr()` → correlation coefficient *r* (−1 to +1)
- `c=` + `cmap=` + `fig.colorbar()` → color by a 3rd variable
- `s=` → size by a 4th variable

---

### 8. Subplots — `08_subplots.py`
**What:** Multiple charts in one figure (like a dashboard).
**How:**
```python
fig, axes = plt.subplots(2, 2)      # grid
axes[0, 1].bar(...)                  # access by [row, col]
fig.suptitle("Overall title")
```
For uneven layouts use **GridSpec**:
```python
gs = fig.add_gridspec(2, 2)
top = fig.add_subplot(gs[0, :])     # spans full first row
```

---

### 9. Introduction to Seaborn — `09_intro_seaborn.py`
**What:** A library built **on top of Matplotlib** for statistical charts with nicer defaults.
**Why use it:**
- Works directly with pandas: `sns.scatterplot(data=df, x="col1", y="col2")`
- `hue="gender"` groups and colors automatically (no manual loop)
- Themes: `sns.set_theme(style="whitegrid")`
- Regression lines built in: `sns.lmplot()`

**Demo:** the same grouped scatter plot made in Matplotlib (loop) vs Seaborn (one line).

---

### 10. Basic Plot Types in Seaborn — `10_basic_plot_types_seaborn.py`
| Type | Function | Shows |
|---|---|---|
| Distribution | `histplot`, `kdeplot` | Shape of one variable |
| Categorical | `countplot` | Count per category |
| Categorical | `barplot` | Mean per category + error bar |
| Categorical | `boxplot` | Median, quartiles, outliers |
| Categorical | `violinplot` | Box + full distribution shape |
| Categorical | `stripplot` | Every individual point |
| Relational | `lineplot` | Trends (needs long-format data → `df.melt()`) |
| Matrix | `heatmap` | Correlation table as colors |
| Multi | `pairplot` | Every pair of numeric columns at once |

**Axes-level vs Figure-level:** most functions accept `ax=` to go into a subplot; `lmplot` and `pairplot` create their own figure.

---

## 🧪 Practice Ideas
1. In `03_bar_charts.py`, make a **stacked** bar chart using `bottom=`.
2. In `06_histograms.py`, add `density=True` and compare.
3. In `08_subplots.py`, build a 3×2 dashboard with all chart types.
4. In `10_basic_plot_types_seaborn.py`, try `sns.swarmplot` and `sns.jointplot`.
5. Replace a `get_...()` function in `common.py` with `pd.read_csv("your_file.csv")` to use real data.
