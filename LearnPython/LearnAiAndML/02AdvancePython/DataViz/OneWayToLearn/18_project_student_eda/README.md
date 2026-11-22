# Lecture 18: Project: exploratory data analysis (EDA) with Seaborn

Run: `python lecture.py` → 8 charts in `output/` + printed findings

**Goal:** explore a student dataset (400 students: study hours, sleep, score, gender, grade) the way an analyst would, by asking **one question per step**, drawing the chart that answers it, and **writing down the finding**. Exploration ends with a one-page summary figure for a presentation.

## The EDA workflow

| Step | Question | Charts | Lecture |
|------|----------|--------|---------|
| 0 | What's in the data? Any missing values? | `head`, `describe` (no chart yet) | 00 |
| 1 | How is each numeric variable distributed? | `histplot(kde=True)` + mean line | 11 |
| 2 | Are the groups balanced? | `countplot` with `hue`, `bar_label` | 12 |
| 3 | What relates to what? | `pairplot(hue=..., corner=True)`, correlation `heatmap` | 14 |
| 4 | How strong is the main relationship? | `lmplot` + pass-mark reference lines | 13 |
| 5 | Do groups differ? | `boxplot` with hue; `violinplot` + `stripplot` by study band | 12 |
| 6 | Do two factors combine? | pivot-table `heatmap`; scatter with colour and size | 13, 14 |
| 7 | Communicate | `subplot_mosaic` summary with insight titles | 08, 09 |

## Findings (printed by `lecture.py`)

1. Study hours are spread evenly from 0 to 10; sleep is bell-shaped around 6.9 h; the mean score is 59.5, and **13% fail** (score < 40).
2. The groups are balanced: 96–102 students per grade and 200/200 by gender. Comparisons are fair.
3. **Study hours are the strongest driver** of score (r = 0.89); sleep has a weak positive link (r = 0.21).
4. Each extra study hour adds **≈ 5.1 points**. On average about 1.1 h/day reaches the pass mark. The slope is nearly the same for both genders (4.9 vs 5.2).
5. **Grade level barely matters** (means 59–60). Study time matters a lot: the pass rate is **60%** for 0–3 h vs **100%** for 6–10 h.
6. **Sleep adds on top of study:** in every study band, students sleeping > 8 h outscore those sleeping < 6 h by **8–10 points**.

> ⚠️ This is observational data (here, generated). Charts show **associations**. Concluding "study more *causes* higher scores" needs an experiment or careful causal analysis.

## Good EDA habits shown here

- **Start broad, then zoom in:** distributions → relationships → groups → interactions.
- Engineer helpful columns for plotting (`pd.cut` into study and sleep **bands**; a pass/fail `result`).
- Use **reference lines** (pass mark, means) so the charts answer the question directly.
- Use a **colour-blind palette** (`sns.set_theme(palette="colorblind")`) and consistent category orders (`order=ORDER`).
- **Write each finding down immediately**, with numbers. The final summary figure repeats only the key messages.

## Extension exercises

1. Add a step: "Is sleep different between genders or grades?" Pick the chart yourself.
2. Draw an `ecdfplot` of score by study band and read off each band's median.
3. Replace the dataset with a real CSV (e.g. a public student-performance dataset). Which steps still work unchanged?
4. Turn the summary figure into a 2×2 layout with a fourth panel showing the sleep effect.

**Next →** [Lecture 19: Practice exercises](../19_practice_exercises/)
