# Lecture 02: Line plots

Run: `python lecture.py`

## When to use a line plot

A line connects values in **order**, so it's the chart for **trends over time** or any ordered x (distance, dose, epoch). Use it when the *change between points* matters.

❌ Don't connect unordered categories with lines (cities, products): use bars.

## The basic call

```python
fig, ax = plt.subplots()
ax.plot(x, y, color="#1f77b4", linestyle="-", marker="o", linewidth=2, label="Electronics")
ax.legend()
```

## Formatting options

| Argument | Values | Notes |
|----------|--------|-------|
| `color` / `c` | `"red"`, `"tab:blue"`, `"#1f77b4"`, `(0.1, 0.4, 0.8)` | `tab:` colours are the defaults |
| `linestyle` / `ls` | `"-"` solid, `"--"` dashed, `":"` dotted, `"-."` dash-dot, `"none"` | |
| `linewidth` / `lw` | number (points) | 1.5 default |
| `marker` | `"o"` circle, `"s"` square, `"^"` triangle, `"D"` diamond, `"x"`, `"+"`, `"."` | |
| `markersize` / `ms`, `markerfacecolor`, `markeredgecolor` | | hollow markers: `markerfacecolor="white"` |
| `markevery=5` | a marker on every 5th point | for dense lines |
| `alpha` | 0 (invisible) … 1 (solid) | |
| `label` | text for the legend | |
| `drawstyle="steps-post"` | step line | values that stay constant until changing (prices, stock levels) |

Shorthand **format string**: `ax.plot(x, y, "r--o")` = red, dashed, circle markers. It's handy but less readable.

## Making the line tell a story

| Tool | Use |
|------|-----|
| `ax.annotate("Peak", xy=(x, y), xytext=(x2, y2), arrowprops=dict(arrowstyle="->"))` | point at an important value |
| `ax.axhline(y, ls="--")` / `ax.axvline(x)` | target lines, averages, events |
| `ax.axvspan(x1, x2, alpha=0.2)` | shade a period (a campaign, a lockdown) |
| `ax.fill_between(x, low, high, alpha=0.2)` | uncertainty bands, ranges (min–max) |
| `ax.set_ylim(0, 90)` | control the scale |
| `ax.text(x, y, "label")` | label lines directly at their end (often better than a legend) |

## Time series with real dates

Pass `datetime` / pandas `Timestamp` values as x. Matplotlib then uses date-aware ticks. Format them with `matplotlib.dates`:

```python
import matplotlib.dates as mdates
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
```

Daily data is noisy, so add a **rolling average** (`df["visits"].rolling(7).mean()`) to reveal the trend.

## Scales and twin axes

- `ax.set_yscale("log")`: for exponential growth or values spanning orders of magnitude. Equal steps then mean equal *ratios*.
- `ax2 = ax.twinx()`: a second y-axis for a different unit (visits vs signups). ⚠️ Use with care: two scales can be chosen to make *any* lines look correlated (Lecture 16). Colour each axis like its line.

## Common mistakes

| Mistake | Fix |
|---------|-----|
| more than ~5 lines ("spaghetti") | highlight one and grey the rest, or use small multiples (Lecture 08) |
| a legend far from the lines | label the line ends directly |
| unsorted x values → zig-zag lines | `df.sort_values("x")` first |
| `x` as strings with thousands of dates → unreadable ticks | use real dates + a date locator |

## Exercises

1. Plot Clothing with a dash-dot line, diamond markers and hollow white faces.
2. Annotate the **lowest** Clothing month.
3. Shade the campaign period on the visits chart with `axvspan`.
4. Plot `x`, `x²`, `2ˣ` from 1 to 20 on linear and log y-scales side by side.

**Next →** [Lecture 03: Bar charts](../03_bar_charts/)
