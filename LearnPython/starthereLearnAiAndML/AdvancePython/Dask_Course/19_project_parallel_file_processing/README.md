# Lecture 19: Project: parallel processing of custom work

Run: `python lecture.py`. It writes `output/file_reports.csv` and `output/simulation.csv`.

Not every job is a DataFrame query. This project parallelises **custom Python work** with the tools from Lectures 03 and 14:

## Part A: a data-quality report for every file (`dask.delayed`)

For each of the 12 monthly files, a custom function:
1. loads the file with pandas
2. checks quality: rows, missing values, duplicate ids, out-of-range prices, timestamps outside the file's month
3. computes summary statistics
4. returns a one-row dict

```
 file 1 ─► load ─► check ─► summarise ─┐
 file 2 ─► load ─► check ─► summarise ─┼─► combine into one report table
   ...                                 │
 file 12 ─► load ─► check ─► summarise ─┘
```

Sequential vs `delayed` (threads) vs the distributed cluster are timed.

## Part B: a Monte Carlo simulation (futures + `as_completed`)

"If each order has a 2% chance of being returned, what's the distribution of yearly refunds?"

- 40 simulation runs, each a full simulated year (12 × 2 million orders, NumPy), submitted with `client.map`
- results are collected **as they finish** (`as_completed`), with a live progress counter
- a big shared input (the price list) is sent **once** with `client.scatter`

## Measured (2-core machine)

| Work | Sequential | Dask |
|------|-----------|------|
| Part A: 12 file reports | 2.9 s | threads 2.6 s · **cluster 1.7 s** |
| Part B: 40 simulated years | 4.0 s | **cluster 2.1 s** (≈ 2× on 2 cores) |

**Task size matters.** An earlier version simulated one *month* per task (~1–7 ms each). Dask gave **no speed-up at all**, because per-task overhead ate the gain. Making each task a full *year* (~100 ms) fixed it. Aim for tasks of at least ~100 ms.

## Patterns worth copying

| Pattern | Why |
|---------|-----|
| One task = one file / one scenario | tasks big enough to beat the overhead |
| Return small results (dicts, numbers) | cheap to send back |
| Combine at the end with `pd.DataFrame(list_of_dicts)` | no growing DataFrames in a loop |
| `pure=False` for random simulations | otherwise identical calls would be cached |
| `scatter` shared inputs | not re-sent with every task |
| `as_completed` | progress reporting; start using results early |

## Extension exercises

1. Add a check: orders with `units * unit_price > 2,00,000`.
2. Make the report flag any file whose missing-value rate is above 0.12%.
3. Run 200 simulations and plot a histogram of the refund totals.
4. Replace the threads run in Part A with `scheduler="processes", chunksize=1` and compare.

**Next →** [Lecture 20: Recap & cheat sheet](../20_recap_cheatsheet/)
