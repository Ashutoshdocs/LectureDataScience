# Lecture 05: Stack plots (stacked area charts)

Run: `python lecture.py`

## What a stack plot shows

Each category is a coloured **band** stacked on top of the previous ones, so:
- the **top edge** is the **total**,
- each band's **thickness** is that category's contribution.

It answers two questions at once: **how does the total change over time, and what is it made of?**

```python
ax.stackplot(x, y1, y2, y3, labels=["A", "B", "C"], alpha=0.85)
ax.legend(loc="upper left")
```

You can pass the series as separate arguments or as one 2-D array/list (`ax.stackplot(x, df[cols].T)`). `colors=[...]` sets the band colours.

## Two versions

| Absolute stack | 100% stack |
|----------------|------------|
| raw values | each row divided by its total × 100 |
| shows **growth of the total** | shows **shift in shares** |
| "sales grew from 114 to 163" | "Groceries' share fell from 39% to 29%" |

```python
share = df[cols].div(df[cols].sum(axis=1), axis=0) * 100
```

## The big limitation

Only the **bottom band** sits on a flat baseline. Every band above it rides on a wavy baseline, so its **own trend is hard to read**. In `lecture.py`, Groceries is flat, but in a stack it *looks* like it rises and falls with the bands beneath.

**When you need to compare individual trends, use separate lines (or small multiples). Use a stack when the total and the composition matter more.**

## Options and tips

| Tip | How |
|-----|-----|
| put the most stable / important series at the **bottom** | order of arguments |
| ≤ 5 bands | more becomes unreadable |
| label bands directly inside | `ax.text` at the band's middle |
| `baseline="wiggle"` | **streamgraph**: a centred, flowing look; decorative, hard to read exactly |
| x must be numeric or dates | use `np.arange(len(df))` + `set_xticks(x, labels)` for month names |

## Exercises

1. Put Groceries at the bottom of the stack. Does its trend become readable?
2. Add the total as a dashed black line on top of the absolute stack.
3. Make a streamgraph with `baseline="wiggle"`.
4. Turn the 100% stack into a 100% stacked **bar** chart (Lecture 03). Which do you prefer for 12 months?

**Next →** [Lecture 06: Histograms](../06_histograms/)
