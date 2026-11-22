# Lecture 17: Project: a one-page sales dashboard (Matplotlib)

Run: `python lecture.py` → `output/17_sales_dashboard.png`

**Goal:** combine everything from Part 2 into one professional, management-ready dashboard: KPI tiles, a trend, a share, a target comparison, a heatmap, a time series, and a pattern chart.

## Layout: plan it before you code

```
┌─────────┬─────────┬─────────┬─────────┐
│ KPI 1   │ KPI 2   │ KPI 3   │ KPI 4   │   ← headline numbers first
├─────────┴─────────┴─────────┼─────────┤
│ monthly trend (stacked)     │ share   │   ← most important chart: biggest, top-left
├───────────────────┬─────────┴─────────┤
│ regions vs target │ product mix heat  │
├───────────────────┴─────────┬─────────┤
│ daily visits + 7-day avg    │ weekday │
└─────────────────────────────┴─────────┘
```

Built with **`plt.subplot_mosaic`** (Lecture 08): the layout *is* a list of names, `height_ratios` makes the KPI row short, and `layout="constrained"` handles the spacing and colourbars.

## Techniques used, and where you learned them

| Element | Technique | Lecture |
|---------|-----------|---------|
| KPI tiles | an Axes with `set_axis_off()`, a `Rectangle` patch, text in `transAxes` coordinates; green/red subtext | 09 |
| monthly trend | `stackplot` + a total line + `annotate` for the best month + `FuncFormatter` | 02, 05, 09 |
| market share | donut (`wedgeprops={"width": ...}`), one highlight colour, centre text | 04 |
| regions vs target | sorted `barh`, colour by above/below target, a target marker (`scatter` with `marker="\|"`), `bar_label` with % | 03 |
| product mix | `imshow` heatmap with value text and contrast-aware text colour, colourbar | 09, 14 |
| daily visits | raw line in grey + 7-day `rolling` mean, `axvspan` for the campaign, date locators | 02 |
| weekday pattern | bars, weekend muted | 03 |
| consistency | one `BRAND` colour dictionary, left-aligned titles, spines removed | 09, 15 |

## Dashboard design rules applied

1. **Most important information top-left**; KPIs first.
2. **One colour system**: each category always has the same colour; grey for context.
3. **Insight titles and annotations**, so the reader doesn't have to hunt for the point.
4. **Formatted numbers** (`Rs 1,666k`, `2.6k`, `+14.4%`).
5. **Consistent alignment** (titles `loc="left"`) and generous white space.
6. KPI subtext coloured **green/red** by direction.

## Results (printed by `lecture.py`)

- Total sales Rs 1,666k; **H2 is +14.4% over H1**, with Electronics driving the growth.
- **North is the only region below target** (−7%); West leads (+15%).
- Weekend traffic is **25% lower** than weekdays.
- The April campaign (11–17 Apr) lifted daily visits **1.9×** for a week; the 7-day average makes the underlying growth visible.

## Extension exercises

1. Add a fifth KPI tile, "Best region", and make the layout 5 columns wide.
2. Replace the `imshow` heatmap with `sns.heatmap` (keep everything else in Matplotlib).
3. Export the dashboard as an A4 landscape PDF (`figsize=(11.69, 8.27)`) and check that it's readable.
4. Wrap the whole thing in a function `build_dashboard(sales, visits, regional)` so it can be regenerated every month.

**Next →** [Lecture 18: Project: student EDA](../18_project_student_eda/)
