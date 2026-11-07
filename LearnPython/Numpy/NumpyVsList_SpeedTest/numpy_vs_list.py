"""
NUMPY VS PYTHON LISTS — PERFORMANCE DEMO
========================================
Goal:
  Show why NumPy is often much faster than ordinary Python loops for
  large numerical datasets.

Install:
  python -m pip install numpy

Run:
  python numpy_vs_list.py

The program:
  1. Creates the same deterministic demo data for both approaches.
  2. Calculates (price * quantity) + tax for every record.
  3. Compares a normal Python-list loop with NumPy vectorized operations.
  4. Checks that both approaches produce the same answers.
  5. Reports median execution times and speed-up.

Important:
  NumPy is not automatically faster for every tiny task. Its advantage is
  strongest for large numerical arrays and operations that can be vectorized.
"""

import statistics
import time

import numpy as np


# ------------------------- DEMO CONFIGURATION -------------------------
DATA_SIZE = 1_000_000
REPEATS = 5
WARMUPS = 1


def create_demo_data(size):
    """Create deterministic data so both methods receive identical values."""
    prices = [float((i % 1000) + 1) for i in range(size)]
    quantities = [float((i % 10) + 1) for i in range(size)]
    tax_rates = [0.18] * size
    return prices, quantities, tax_rates


def python_list_calculation(prices, quantities, tax_rates):
    """Traditional Python: loop through each record and calculate its total."""
    totals = []
    for i in range(len(prices)):
        subtotal = prices[i] * quantities[i]
        total = subtotal + (subtotal * tax_rates[i])
        totals.append(total)
    return totals


def numpy_calculation(prices_np, quantities_np, tax_rates_np):
    """NumPy: perform the same calculation on whole arrays at once."""
    subtotals = prices_np * quantities_np
    totals = subtotals + (subtotals * tax_rates_np)
    return totals


def benchmark(function, *args):
    """Warm up, then return the median runtime and the last result."""
    for _ in range(WARMUPS):
        function(*args)

    timings = []
    result = None
    for _ in range(REPEATS):
        start = time.perf_counter()
        result = function(*args)
        timings.append(time.perf_counter() - start)

    return statistics.median(timings), result


def main():
    print("=" * 68)
    print("             PYTHON LISTS vs NUMPY — LIVE BENCHMARK")
    print("=" * 68)

    prices, quantities, tax_rates = create_demo_data(DATA_SIZE)

    # Convert the same list data into NumPy arrays.
    prices_np = np.array(prices, dtype=np.float64)
    quantities_np = np.array(quantities, dtype=np.float64)
    tax_rates_np = np.array(tax_rates, dtype=np.float64)

    print(f"\nDemo records : {DATA_SIZE:,}")
    print(f"Data type    : numeric sales records")
    print(f"Calculation  : (price * quantity) + 18% tax")
    print(f"Runs         : {REPEATS} measured runs; median displayed")

    print("\n[1] Running normal Python list loop...")
    python_time, python_result = benchmark(
        python_list_calculation, prices, quantities, tax_rates
    )

    print("[2] Running NumPy vectorized calculation...")
    numpy_time, numpy_result = benchmark(
        numpy_calculation, prices_np, quantities_np, tax_rates_np
    )

    # Validate results before presenting the speed comparison.
    np.testing.assert_allclose(
        np.asarray(python_result), numpy_result, rtol=1e-12, atol=1e-12
    )

    speedup = python_time / numpy_time if numpy_time else float("inf")

    print("\n" + "-" * 68)
    print("RESULTS")
    print("-" * 68)
    print(f"Python list loop : {python_time:.6f} seconds")
    print(f"NumPy operation  : {numpy_time:.6f} seconds")
    print(f"NumPy speed-up   : {speedup:.2f}x faster in this run")

    print("\nFirst 5 calculated totals (both methods match):")
    for i in range(5):
        print(
            f"Record {i + 1}: "
            f"Python = {python_result[i]:.2f} | "
            f"NumPy = {numpy_result[i]:.2f}"
        )

    print("\n" + "-" * 68)
    print("WHY CAN NUMPY BE FASTER?")
    print("-" * 68)
    print("1. Python lists store references to Python objects.")
    print("2. A Python loop performs indexing, object handling and arithmetic")
    print("   repeatedly at the Python interpreter level.")
    print("3. NumPy stores homogeneous numeric data in compact typed arrays.")
    print("4. Vectorized operations run in optimized compiled code, reducing")
    print("   Python-level loop and object-handling overhead.")
    print("\nTeaching note:")
    print("- For a tiny dataset, setup/conversion overhead can reduce the gain.")
    print("- Here, conversion is done before timing so we compare the calculations.")
    print("- Real applications must include conversion cost if data starts as lists.")
    print("- NumPy speed depends on operation, data size, hardware and environment.")
    print("=" * 68)


if __name__ == "__main__":
    main()
