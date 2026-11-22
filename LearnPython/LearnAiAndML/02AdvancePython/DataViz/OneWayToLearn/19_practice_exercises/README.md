# Lecture 19: Practice exercises (15, auto-checked)

| File | What it is |
|------|------------|
| `exercises.py` | **Your work.** 15 functions; each builds a chart and **returns the Figure**. Docstrings say exactly what is checked. |
| `solutions.py` | Reference solutions. Try first! |
| `lecture.py` | The checker. It inspects the returned figures (lines, bars, wedges, text, titles, labels, scales, spines) and saves every passing chart to `output/`. |

```bash
python lecture.py              # checks solutions.py -> 15 / 15
python lecture.py exercises    # checks YOUR file
```

```
  ✔ 01 line + labels
  ✘ 06 stacked bars       stack tops must equal the monthly totals (use bottom=)
  ✘ 11 log scale          y-scale is 'linear', expected 'log'
  Score: 13 / 15
```

## The exercises

| # | Function | Skill | Lecture |
|---|----------|-------|---------|
| 01 | `ex01_line` | line, marker, title, axis labels | 02 |
| 02 | `ex02_three_lines_legend` | several series + legend | 02 |
| 03 | `ex03_annotate_peak` | `annotate` with an arrow at the maximum | 02 |
| 04 | `ex04_sorted_barh` | sorted horizontal bars, largest at the top, `bar_label` | 03 |
| 05 | `ex05_grouped_bars` | grouped bars with offsets and month ticks | 03 |
| 06 | `ex06_stacked_bars` | stacked bars with `bottom=` | 03 |
| 07 | `ex07_donut` | donut with centre text | 04 |
| 08 | `ex08_hist_mean` | histogram with explicit bins + a mean line | 06 |
| 09 | `ex09_scatter_trend` | scatter + `polyfit` trend + r in the title | 07 |
| 10 | `ex10_subplots_shared` | 1×3 subplots with `sharey=True` | 08 |
| 11 | `ex11_log_scale` | log y-axis | 02 |
| 12 | `ex12_sns_box` | Seaborn boxplot with category `order` | 12 |
| 13 | `ex13_sns_heatmap` | correlation heatmap with a fixed −1…1 scale | 14 |
| 14 | `ex14_sns_hue_scatter` | `hue` grouping | 10 |
| 15 | `ex15_declutter` | spines, left title, y-axis from 0 | 09 |

These include the practice ideas from your original project (stacked bars with `bottom=`, `density`, dashboards), plus more.

## Rules

- **Return the figure** (`return fig`). Don't call `plt.show()` inside the functions.
- Create your own figure in each function (`fig, ax = plt.subplots()`), and for Seaborn pass `ax=ax`.
- Open the saved PNGs in `output/` to see your charts.

**Next →** [Lecture 20: Quick revision](../20_quick_revision/)
