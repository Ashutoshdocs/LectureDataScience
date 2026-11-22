# Lecture 20 — Project: estimate π — loop vs NumPy

Run: `python lecture.py`

## The idea: Monte Carlo

Throw random darts at a 1 × 1 square. A quarter circle of radius 1 fills π/4 of that square.

```
  1 ┌──────────┐
    │ ····     │      a dart (x, y) is INSIDE the quarter circle
    │ ·····    │      when  x² + y² ≤ 1
    │ ······   │
    │ ·······  │      fraction inside ≈ π / 4
    │ ········ │      so   π ≈ 4 × fraction inside
  0 └──────────┘
    0          1
```

This is a **Monte Carlo** simulation — using random sampling to estimate a quantity. It's used in finance (risk), physics, engineering, games and AI.

## Two implementations

| Plain Python | NumPy |
|-------------|-------|
| Loop half a million times | Generate **all** darts in one call |
| Two random calls, a check and a counter per dart | One mask: `x*x + y*y <= 1` |
| Count hits by hand | `np.mean(mask)` — the mean of a True/False array = fraction True |

```python
rng = np.random.default_rng(1)
x, y = rng.random(n), rng.random(n)
np_pi = 4 * np.mean(x * x + y * y <= 1)
```

Same answer, a fraction of the time, half the code. Simulations with millions of samples are only practical because of this.

## Accuracy grows with more darts

The error shrinks roughly like 1/√n — 100× more darts ≈ 10× more accurate. `lecture.py` prints a table for n = 100 … 10 000 000.

## Expected output (desktop; times vary)

```
Python: pi = 3.1421 in   82.0 ms
NumPy : pi = 3.1434 in    5.7 ms
Speed-up: about 14x
```

## Extension exercises

1. Set `n` to 5 000 000 for the NumPy part only. How close to 3.14159 do you get?
2. Use `np.pi` to print the error of each estimate.
3. Estimate the area under `y = x²` from 0 to 1 the same way (answer: 1/3).

<details><summary>Hints</summary>

```python
abs(np_pi - np.pi)
x, y = rng.random(n), rng.random(n); np.mean(y <= x**2)   # ≈ 0.3333
```
</details>

**Next →** [Lecture 21: Recap & cheat sheet](../21_recap_cheatsheet/)
