# Lecture 17 — Random numbers & simulation

Run: `python lecture.py`

Random data is essential for simulations, games, sampling, testing code, and machine learning (shuffling data, initialising weights).

## The modern way: a Generator

```python
rng = np.random.default_rng(seed=42)
```

Create one generator, then call methods on it:

| Call | Gives |
|------|-------|
| `rng.integers(low, high, size)` | whole numbers, `high` **excluded** |
| `rng.random(size)` | decimals in [0, 1) |
| `rng.uniform(low, high, size)` | decimals in [low, high) |
| `rng.normal(mean, sd, size)` | bell-curve values |
| `rng.choice(arr, size, replace=True/False)` | random picks from `arr` |
| `rng.choice(arr, size, p=[...])` | picks with given probabilities |
| `rng.shuffle(arr)` | shuffle **in place** |
| `rng.permutation(arr)` | shuffled **copy** |

`size` can be a tuple for 2D: `rng.integers(0, 10, size=(3, 4))`.

## Why a seed?

`seed=42` makes the "random" numbers **repeat exactly** every run, so results can be checked and shared. Remove the seed to get new numbers each time.

> Computers generate *pseudo*-random numbers from a formula. The seed is the starting point of that formula.

## Old style you'll still see

```python
np.random.seed(0)
np.random.randint(1, 7, 10)
np.random.rand(3)
```
This legacy API still works, but new code should use `default_rng`. (The two produce **different** numbers for the same seed.)

## Simulation pattern

1. Generate *all* random trials at once as an array.
2. Use vectorized operations / masks to evaluate them.
3. Aggregate with `mean`, `sum`, `bincount`.

Example in `lecture.py`: roll two dice 100 000 times and estimate the probability of rolling a total of 7 (theory: 6/36 ≈ 0.1667).

## Exercises

1. Remove `seed=42` and run twice. What changes?
2. Simulate 20 coin flips with `rng.integers(0, 2, size=20)`. How many heads?
3. Roll 600 dice and count each face with `np.bincount`.
4. Deal a 5-card hand from 52 cards without replacement.

<details><summary>Solutions</summary>

```python
rng = np.random.default_rng()            # new numbers every run
flips = rng.integers(0, 2, size=20); flips.sum()
np.bincount(rng.integers(1, 7, 600))[1:] # roughly 100 each
rng.choice(52, size=5, replace=False)
```
</details>

**Next →** [Lecture 18: Project — class report card](../18_project_report_card/)
