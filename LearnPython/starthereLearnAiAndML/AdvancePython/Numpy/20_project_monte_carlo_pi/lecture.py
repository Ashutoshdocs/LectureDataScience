"""Lecture 20 — Project: estimate pi with Monte Carlo, plain Python vs NumPy."""
import random
import time
import numpy as np

n = 500_000

t = time.perf_counter()                  # --- plain Python ---
inside = 0
for _ in range(n):
    x, y = random.random(), random.random()
    if x * x + y * y <= 1:
        inside += 1
py_pi, py_t = 4 * inside / n, time.perf_counter() - t

t = time.perf_counter()                  # --- NumPy ---
rng = np.random.default_rng(1)
x, y = rng.random(n), rng.random(n)
np_pi = 4 * np.mean(x * x + y * y <= 1)
np_t = time.perf_counter() - t

print(f"Python: pi = {py_pi:.4f} in {py_t * 1000:6.1f} ms")
print(f"NumPy : pi = {np_pi:.4f} in {np_t * 1000:6.1f} ms")
print(f"Speed-up: about {py_t / np_t:.0f}x")

print("\n--- Error vs the true value ---")
print(f"Python error: {abs(py_pi - np.pi):.5f}")
print(f"NumPy  error: {abs(np_pi - np.pi):.5f}")

print("\n--- More darts, better estimate (error ~ 1/sqrt(n)) ---")
print(f"{'darts':>12} {'estimate':>10} {'error':>10}")
for k in [100, 10_000, 1_000_000, 10_000_000]:
    xs, ys = rng.random(k), rng.random(k)
    est = 4 * np.mean(xs * xs + ys * ys <= 1)
    print(f"{k:>12,} {est:>10.5f} {abs(est - np.pi):>10.5f}")

print("\n--- Same trick: area under y = x^2 from 0 to 1 ---")
xs, ys = rng.random(1_000_000), rng.random(1_000_000)
print(f"estimate {np.mean(ys <= xs ** 2):.4f} | exact {1/3:.4f}")
