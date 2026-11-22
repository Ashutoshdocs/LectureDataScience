# Lecture 22: Project: student result system

Run: `python lecture.py`

This project turns raw marks into report cards and a class summary through a **pipeline of small, composable functions**. Each step does one job, and the output of one step is the input of the next.

```
 raw text ──parse──▶ records ──validate──▶ clean records ──enrich──▶ total / % / grade / result
                                                                         │
                         report cards ◀──format──┤──rank──▶ class toppers & subject stats
```

## Pipeline stages

| Stage | Function(s) | Lectures used |
|-------|-------------|---------------|
| Parse | `parse_line`, `parse_all` (generator) | 17, 18 |
| Validate | `validate_marks` raises `InvalidMarks`; bad rows are collected | 18 |
| Enrich | `total`, `percentage`, `grade`, `result_status` (all **pure**) | 04, 19 |
| Rules | `GRADE_BANDS` table + `grade()` with early returns | 04, 10 |
| Combine | `compose(*funcs)` builds one function from many | 10, 13 |
| Rank | `rank_students(students, key=...)` with `sorted` + `lambda` | 11, 12 |
| Stats | `subject_stats(students)` uses `zip`, `max`, `min`, `sum` | 12 |
| Report | `report_card(student, *, width=40)` | 08 |
| Extras | `@timed` decorator; `make_grace_marks(n)` closure | 13, 14 |

## Rules used

- 5 subjects, each 0–100.
- Pass needs **≥ 35 in every subject**. Otherwise the result is "FAIL (subject list)".
- Grade from the percentage: A+ ≥ 90, A ≥ 80, B ≥ 70, C ≥ 60, D ≥ 50, E ≥ 35, else F. A student who fails any subject gets F whatever the percentage.
- Optional grace marks (up to N) can lift a subject from just below 35 to pass.

## Why build it as a pipeline?

- Each function can be **tested on its own** (the file runs `assert` tests first).
- Rules change in **one place**: edit `GRADE_BANDS` or `PASS_MARK`.
- Stages can be **reused** or swapped: grace marks are added by inserting one function into the pipeline.

## Extension exercises

1. Read the marks from a CSV file with `csv.DictReader`.
2. Add a "distinction" flag for students with ≥ 75 in every subject.
3. Write `subject_toppers(students)` that returns the best student per subject.
4. Make the pass mark a parameter that flows through the whole pipeline.

**Next →** [Lecture 23: Practice exercises](../23_practice_exercises/)
