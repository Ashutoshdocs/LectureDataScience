# Lecture 04: Pie & donut charts

Run: `python lecture.py`

## When to use a pie

A pie shows **parts of one whole that add up to 100%**. It works only when:

- there are **few slices** (≤ 5–6),
- the shares are **clearly different**, or you want to stress one dominant share ("Brand A has a third of the market"),
- the values really are parts of a total. Never use a pie for unrelated numbers.

## Why pies are often a bad idea

People compare **angles and areas** much less accurately than **lengths**. With slices of 24%, 26% and 25%, nobody can rank them from a pie, but anyone can from a bar chart (`lecture.py` shows this side by side). Comparing two pies (this year vs last year) is even harder.

> Rule of thumb: if you need to *compare* parts, use a (sorted) bar chart. If you need to show *one part's share of a whole*, a pie or donut is fine.

## The call

```python
ax.pie(sizes, labels=labels,
       autopct="%1.1f%%",          # percentage text inside slices
       startangle=90,              # first slice starts at 12 o'clock
       counterclock=False,         # go clockwise (reads like a clock)
       explode=[0.1, 0, 0, 0, 0],  # pull slice 1 out by 10% of the radius
       colors=[...],
       wedgeprops={"edgecolor": "white", "linewidth": 2},
       pctdistance=0.75,           # where the % text sits (0 = centre, 1 = edge)
       labeldistance=1.1)
ax.axis("equal")                   # a circle, not an oval (often automatic now)
```

| Argument | Effect |
|----------|--------|
| `autopct` | `"%1.0f%%"` → `32%`; can be a function: `lambda p: f"{p:.0f}%\n({p * total / 100:.0f})"` |
| `explode` | emphasise a slice; use sparingly (one slice) |
| `shadow=True` | 3-D-looking shadow, mostly decorative (avoid in professional charts) |
| `wedgeprops={"width": 0.4}` | turns it into a **donut** (ring thickness = 40% of the radius) |
| `textprops={"fontsize": 11}` | style all text |

## Donut charts

A donut is a pie with a hole: `wedgeprops={"width": 0.4}`. The centre is a natural place for a **total or headline** (`ax.text(0, 0, "₹4.2 Cr", ha="center", va="center")`). Readers judge arc length a little better than angle, but the same limits apply.

## Tips

- Sort the slices from largest to smallest, starting at 12 o'clock and going clockwise.
- Combine tiny slices into "Others".
- Label slices directly; avoid a separate legend if possible.
- Use one strong colour for the slice you're talking about and muted colours for the rest.

## Exercises

1. Show the value and the percentage in each slice using an `autopct` function.
2. Make a donut with the total market size in the centre.
3. Build a nested donut: the inner ring is brands, the outer ring is each brand split into online/offline.
4. Convert the pie into a horizontal, sorted bar chart. Which is easier to read?

**Next →** [Lecture 05: Stack plots](../05_stack_plots/)
