# NumPy — From Zero to Confident

A hands-on NumPy course in 22 short lectures (00–21). Every lecture folder has:

| File | What it is |
|------|------------|
| `README.md` | The lesson: concepts, diagrams, tables, common mistakes, exercises (with solutions) |
| `lecture.py` | Runnable code for the lesson — read it, run it, change it |

## How to use this course

1. **Install Python 3.9+** (check with `python --version`).
2. **Install NumPy** from your terminal (not inside Python):
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Go through the folders **in order**. For each lecture:
   - Read `README.md`
   - Run the code: `python lecture.py`
   - Do the exercises at the bottom of the README, editing `lecture.py` or a new file

## Course map

| # | Lecture | Big idea |
|---|---------|----------|
| 00 | [Prerequisites](00_prerequisites/) | The Python you need first: lists, loops, functions, comprehensions, modules |
| 01 | [What is NumPy?](01_what_is_numpy/) | The `ndarray`: a grid of same-typed numbers |
| 02 | [List vs array](02_list_vs_array/) | `+` and `*` mean different things |
| 03 | [Why it's fast](03_why_fast_speed/) | Compiled loops, no per-item type checks, packed memory |
| 04 | [Why it's compact](04_why_compact_memory/) | Raw numbers vs pointers to objects |
| 05 | [Vectorization](05_vectorization/) | Say *what*, not *how* — replacing loops |
| 06 | [Creating arrays](06_creating_arrays/) | `array`, `zeros`, `ones`, `full`, `arange`, `linspace`, `eye` |
| 07 | [Shape & dtype](07_shape_and_dtype/) | `ndim`, `shape`, `size`, `astype`, overflow |
| 08 | [Indexing & slicing](08_indexing_and_slicing/) | `a[i]`, `a[i:j]`, `m[r, c]`, `m[:, c]` |
| 09 | [Boolean masks](09_boolean_masks/) | Filtering with conditions, `&`, `|`, `~` |
| 10 | [Views vs copies](10_views_vs_copies/) | The slice trap and `.copy()` |
| 11 | [Element-wise maths & ufuncs](11_elementwise_math_ufuncs/) | `np.sqrt`, `np.round`, `np.where` … |
| 12 | [Broadcasting](12_broadcasting/) | Combining different shapes |
| 13 | [Matrix operations](13_matrix_operations/) | `@` vs `*`, dot product, transpose |
| 14 | [Statistics](14_statistics/) | `sum`, `mean`, `median`, `std`, `percentile`, `cumsum`, `diff` |
| 15 | [The axis argument](15_axis_argument/) | Rows vs columns in 2D data |
| 16 | [Reshape, sort & join](16_reshape_sort_join/) | `reshape`, `sort`, `argsort`, `concatenate`, `unique` |
| 17 | [Random numbers](17_random_numbers/) | `default_rng`, seeds, simulations |
| 18 | [Project: class report card](18_project_report_card/) | 2D data, axis, grades with `np.where` |
| 19 | [Project: weather week](19_project_weather_week/) | Parallel arrays + masks |
| 20 | [Project: estimate π](20_project_monte_carlo_pi/) | Monte Carlo — loop vs NumPy race |
| 21 | [Recap & cheat sheet](21_recap_cheatsheet/) | Everything on one page |

## Run everything at once

```bash
python run_all.py
```

## A note on output differences

Outputs shown in the READMEs were produced with **NumPy 2.x on a 64-bit desktop**. You may see:
- `int32` instead of `int64` on some Windows / 32-bit setups
- Different timing numbers in the speed lectures (the *gap* is what matters)
- `np.int64(10)` instead of `10` when you type an expression in the interactive shell (NumPy 2 shows the type; `print()` shows just the number)
