# Lecture 19 — Project: weather week

Run: `python lecture.py`

A week of weather data stored as **three parallel 1D arrays** that line up by position (index 0 in each is Monday):

| index | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|-------|---|---|---|---|---|---|---|
| `days` | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
| `max_c` | 31.2 | 33.8 | 35.1 | 36.4 | 34.0 | 29.5 | 30.8 |
| `rain_mm` | 0 | 0 | 2.5 | 0 | 12.0 | 30.5 | 4.0 |

## The key pattern

> Build a **mask** from one array, then use it to pick from **another** (the day names).

```python
days[rain_mm > 0]                          # which days rained?
days[(max_c > 33) & (rain_mm == 0)]        # hot AND dry
```

That's how NumPy answers "which days…?" questions without a single loop.

> This "parallel arrays + masks" style is exactly how **pandas** works under the hood — a DataFrame is a set of NumPy columns sharing one index.

## Tools used

| Question | Tool |
|----------|------|
| Convert to °F | broadcasting: `max_c * 9 / 5 + 32` |
| Hottest day | `argmax` → index into `days` |
| Above average | mask with `max_c.mean()` |
| Biggest drop | `np.diff(...).min()` |
| Total rain | `.sum()` |
| Running rain total | `np.cumsum` |
| 3-day moving average | `np.convolve(x, np.ones(3)/3, mode="valid")` |

## Expected output (first part)

```
In Fahrenheit: [88.2 92.8 95.2 97.5 93.2 85.1 87.4]
Hottest: Thu 36.4 C
Above average: ['Tue' 'Wed' 'Thu' 'Fri']
Biggest day-to-day drop: -4.5 C
Rainy days: ['Wed' 'Fri' 'Sat' 'Sun']
Total rain: 49.0 mm
Hot AND dry: ['Tue' 'Thu']
```

## Extension exercises

1. Which days had rain over 5 mm?
2. Print the weekly average in °F.
3. Label each day "hot" (> 34), "warm" (> 30) or "cool" with `np.select`.
4. On which day was the rise in temperature largest?

<details><summary>Solutions</summary>

```python
days[rain_mm > 5]                        # ['Fri' 'Sat']
max_f.mean().round(1)                    # 91.3
np.select([max_c > 34, max_c > 30], ["hot", "warm"], default="cool")
days[np.diff(max_c).argmax() + 1]        # 'Tue'
```
</details>

**Next →** [Lecture 20: Project — estimate π](../20_project_monte_carlo_pi/)
