# Python List vs NumPy — Beginner Teaching Demo

## Objective
Demonstrate why NumPy is usually much faster than ordinary Python loops for
large numerical datasets.

## Scenario
Imagine an online shop with 1,000,000 sales records. Each record has:
- Product price
- Quantity
- Tax rate (18%)

For every record, calculate:

```text
subtotal = price * quantity
total = subtotal + (subtotal * tax_rate)
```

The demo calculates the same result in two ways:
1. A traditional Python `for` loop using lists.
2. NumPy vectorized arithmetic using arrays.

## Files
- `numpy_vs_list.py` — complete benchmark program.

## Requirements
Python 3.9+ recommended.

Install NumPy:

```bash
python -m pip install numpy
```

Run:

```bash
python numpy_vs_list.py
```

## What to explain while teaching

### 1. Python list approach
```python
totals = []
for i in range(len(prices)):
    subtotal = prices[i] * quantities[i]
    total = subtotal + (subtotal * tax_rates[i])
    totals.append(total)
```
Python executes the loop and arithmetic through the Python interpreter for
each record.

### 2. NumPy approach
```python
subtotals = prices_np * quantities_np
totals = subtotals + (subtotals * tax_rates_np)
```
The operation is applied to whole arrays. NumPy's optimized compiled routines
do the element-wise work without a Python-level loop for every item.

### 3. Why NumPy can win
- Homogeneous numeric data can be stored in compact typed arrays.
- Less Python object and interpreter overhead.
- Vectorized operations use optimized compiled implementations.
- The same operation can be applied to millions of values concisely.

### 4. Important gotchas
- NumPy is not always faster for tiny datasets.
- Creating NumPy arrays has a cost. This demo converts the data before timing
  so that it compares calculation time separately.
- If your real application starts with Python lists, include conversion time
  when measuring the complete workflow.
- Results vary by CPU, Python/NumPy versions, memory, and system load.
- Both approaches are checked for matching results before the speed-up is shown.

## Suggested classroom questions
1. Why does the Python version need a `for` loop?
2. What does vectorization mean?
3. Why might NumPy lose on only 5 records?
4. Why should we compare identical data and identical calculations?
5. Does NumPy make every Python program faster? Why not?

## Experiment
Change `DATA_SIZE` in the script to:
- `10`
- `1_000`
- `100_000`
- `1_000_000`
- `5_000_000`

Run each time and observe how dataset size affects the performance gap.
Large sizes need more RAM.
