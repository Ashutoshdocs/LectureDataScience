# Lecture 16: Choosing the right chart & avoiding common mistakes

Run: `python lecture.py`: every mistake is drawn **bad (left) vs fixed (right)**.

## Step 1: what question are you answering?

| Question type | Key words | Charts |
|---------------|-----------|--------|
| **Comparison** | "which is biggest", "rank", "vs" | bar (sorted), grouped bar, dot plot |
| **Trend** | "over time", "growth", "season" | line, area; small multiples for many series |
| **Composition** | "share", "% of total", "made of" | stacked bar, 100% bar, pie/donut (few parts), stack plot (over time) |
| **Distribution** | "spread", "typical", "outliers" | histogram, KDE, box, violin, ECDF |
| **Relationship** | "related", "affects", "correlated" | scatter (+ trend), hexbin, pair plot, heatmap of correlations |
| **Part of a table** | many rows × columns | heatmap, small multiples |

## Step 2: how many variables and of what type?

| Variables | Chart |
|-----------|-------|
| 1 numeric | histogram / KDE / box |
| 1 categorical | bar (countplot) |
| numeric × numeric | scatter |
| numeric × time | line |
| categorical × numeric | bar of means (+ error), box, violin, strip |
| categorical × categorical | grouped/stacked bar, heatmap of counts |
| 3+ numeric | pair plot, scatter with colour/size, correlation heatmap |
| anything × a grouping variable | `hue=`, or small multiples (`col=`) |

## How accurately do people read visual encodings?

From most to least precise (Cleveland & McGill): **position on a common scale** → position on separate scales → **length** → angle / slope → area → volume / colour intensity.

So bars and dots beat pies, bubbles and colour shading whenever **exact comparison** matters.

## The ten classic mistakes (all in `lecture.py`)

| # | Mistake | Why it misleads | Fix |
|---|---------|-----------------|-----|
| 1 | **Truncated y-axis on bars** | a 3% difference looks like 3× | bars start at 0 (lines may zoom, if clearly labelled) |
| 2 | **Pie with many slices** | angles can't be compared | sorted horizontal bars |
| 3 | **Spaghetti lines** | 10 tangled lines, colours run out | highlight one + grey the rest, or small multiples |
| 4 | **Dual axes with arbitrary scales** | any two series can be made to "track" each other | two panels, or index both to 100 |
| 5 | **Rainbow (`jet`) colormap** | fake boundaries, unreadable in greyscale or for colour-blind readers | `viridis` / sequential maps |
| 6 | **3-D effects** | perspective distorts sizes | flat 2-D |
| 7 | **Unsorted categories** | the reader has to hunt for the ranking | sort by value (unless the order is natural) |
| 8 | **Overplotting** | thousands of dots hide density | alpha, hexbin, 2-D KDE |
| 9 | **Bar of means hiding the data** | different distributions look identical | box/violin/strip (Lecture 12) |
| 10 | **Missing context**: no title, units, source, labels | the reader can't interpret it | an insight title, axis units, annotations |

Also watch for **cherry-picked time ranges**, **uneven time intervals** drawn as equal steps, **cumulative charts** that hide a slowdown, and **too many decimals**.

## A final checklist before sharing

- [ ] Does the title say the insight?
- [ ] Axis labels with units? Readable tick labels?
- [ ] Correct chart for the question? Bars start at 0?
- [ ] Sorted / logically ordered categories?
- [ ] Colours meaningful, colour-blind safe, ≤ 6 categories?
- [ ] Clutter removed (spines, heavy grids, redundant legend)?
- [ ] Data source and date noted if it's shared outside your team?

## Exercises

1. Find a chart in the news. Which question does it answer? Would another chart type do better?
2. Fix a pie chart of 9 product categories in two different ways.
3. Take the dual-axis example and rebuild it as two stacked panels with a shared x-axis.
4. Rebuild a 3-D bar chart as a 2-D sorted bar chart.

**Next →** [Lecture 17: Project: sales dashboard](../17_project_sales_dashboard/)
