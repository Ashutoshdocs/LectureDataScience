# Data Visualization with Matplotlib & Seaborn: a complete course

Your original 10-topic demo project, reorganised and expanded into a full course: **21 lectures**, each in its own folder with a detailed lesson and a runnable script. It ends with two projects, auto-checked exercises and a revision sheet.

```
dataviz_course/
├── common.py                 # shared: datasets, style, save helper (used by every lecture)
├── run_all.py                # runs every lecture without opening windows
├── requirements.txt
├── 00_why_visualize/
│   ├── README.md             # the lesson: what, why, when, how, pitfalls, exercises
│   ├── lecture.py            # runnable demo
│   └── output/               # charts saved here when you run it (auto-created)
├── 01_matplotlib_anatomy/
└── ...
```

## How to run

```bash
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # macOS / Linux
pip install -r requirements.txt

cd 03_bar_charts
python lecture.py                # chart windows open one by one (close each to continue); PNGs saved to output/

python run_all.py                # from the course folder: runs everything, no windows
                                 # -> "21 of 21 scripts ran successfully, N charts saved"
```

> The zip already contains every chart (142 PNGs) in each lecture's `output/` folder, so you can browse the results before running anything. Re-running a lecture overwrites them.

## Course map

| # | Lecture | You will learn | Your original file |
|---|---------|----------------|--------------------|
| **Part 1: Foundations** | | | |
| 00 | [Why visualize?](00_why_visualize/) | table vs chart, Anscombe's quartet, choosing a chart | `01_intro_data_visualization.py` |
| 01 | [Matplotlib anatomy](01_matplotlib_anatomy/) | Figure / Axes / Axis / Artist, pyplot vs OO, `savefig` | `02_line_plots_matplotlib.py` (part 1) |
| **Part 2: Matplotlib chart types** | | | |
| 02 | [Line plots](02_line_plots/) | styles, markers, annotations, `fill_between`, dates, log scale, twin axes | `02_line_plots_matplotlib.py` |
| 03 | [Bar charts](03_bar_charts/) | vertical, horizontal, grouped, stacked, error bars, labels | `03_bar_charts.py` |
| 04 | [Pie & donut charts](04_pie_and_donut_charts/) | explode, autopct, donuts, when NOT to use pies | `04_pie_charts.py` |
| 05 | [Stack plots](05_stack_plots/) | stacked areas, 100% stacks, stacked area vs lines | `05_stack_plots.py` |
| 06 | [Histograms](06_histograms/) | bins, density, cumulative, step, comparing groups, 2-D histograms | `06_histograms.py` |
| 07 | [Scatter plots](07_scatter_plots/) | trend lines, correlation, colour/size encodings, overplotting, hexbin | `07_scatter_plots.py` |
| 08 | [Subplots & layouts](08_subplots_and_layouts/) | grids, sharex/sharey, GridSpec, `subplot_mosaic`, insets | `08_subplots.py` |
| 09 | [Customization & styling](09_customization_and_styling/) | colours, colormaps, ticks & formatters, spines, legends, text, styles, exporting | new |
| **Part 3: Seaborn** | | | |
| 10 | [Intro to Seaborn](10_intro_seaborn/) | why Seaborn, `hue`, long vs wide data, axes- vs figure-level | `09_intro_seaborn.py` |
| 11 | [Distributions](11_seaborn_distributions/) | `histplot`, `kdeplot`, `ecdfplot`, `rugplot`, `displot` | `10_…seaborn.py` (part) |
| 12 | [Categorical plots](12_seaborn_categorical/) | count, bar, point, box, violin, strip, swarm, `catplot` | `10_…seaborn.py` (part) |
| 13 | [Relational & regression](13_seaborn_relational_and_regression/) | `scatterplot`, `lineplot`, `relplot`, `regplot`, `lmplot`, `residplot` | `09`, `10` (part) |
| 14 | [Matrix & multi-plot grids](14_seaborn_matrix_and_multiplot/) | `heatmap`, `clustermap`, `pairplot`, `jointplot`, `FacetGrid` | `10_…seaborn.py` (part) |
| 15 | [Themes & palettes](15_seaborn_themes_and_palettes/) | `set_theme`, contexts, qualitative/sequential/diverging palettes, colour-blind safety | new |
| **Part 4: Putting it together** | | | |
| 16 | [Choosing charts & common mistakes](16_choosing_charts_and_common_mistakes/) | bad vs fixed: truncated axes, spaghetti, pies, dual axes, rainbow maps | new |
| 17 | [Project: sales dashboard](17_project_sales_dashboard/) | a full KPI dashboard with Matplotlib | new |
| 18 | [Project: student EDA report](18_project_student_eda/) | exploratory analysis with Seaborn, finding insights | new |
| 19 | [Practice exercises](19_practice_exercises/) | 15 auto-checked chart exercises | your "Practice ideas" + more |
| 20 | [Quick revision](20_quick_revision/) | cheat sheet + self-test | new |

## The common file: `common.py`

| Function | Gives you |
|----------|-----------|
| `apply_style()` | one consistent Matplotlib look (grid, font sizes, figure size) |
| `get_monthly_sales()` | 12 months × Electronics, Clothing, Groceries |
| `get_students(n=200)` | study_hours, sleep_hours, score, gender, grade_level |
| `get_market_share()` | brand → % dictionary |
| `get_daily_visits()` | 180 days of website visits & signups (dates, weekly cycle, a campaign spike) |
| `get_restaurant_bills()` | total_bill, tip, size, day, time, smoker (like Seaborn's "tips", but offline) |
| `get_regional_sales()` | quarter × region × product sales vs target, in long format |
| `save_and_show(fig, name)` | saves the PNG into **that lecture's** `output/` folder, then shows the window |

The data is generated with a fixed seed, so you get **the same numbers every run** and need **no internet or CSV files**. To use real data, replace a `get_...()` body with `pd.read_csv("your_file.csv")`.

Tested with Python 3.13, Matplotlib 3.11, Seaborn 0.13, pandas 3.0.
