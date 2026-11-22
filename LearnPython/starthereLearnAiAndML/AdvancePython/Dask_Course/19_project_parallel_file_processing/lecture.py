"""Lecture 19: Project: parallel custom work: per-file quality reports (delayed)
and a Monte Carlo simulation (futures + as_completed + scatter)."""
import logging
import sys
import time
from pathlib import Path
import dask
import numpy as np
import pandas as pd
from dask.distributed import Client, LocalCluster, as_completed

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
OUT = HERE / "output"
sys.path.insert(0, str(DATA))
from make_big_data import ensure_big_data          # noqa: E402

pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 20)
VALID_PRICES = {900, 1500, 3500, 7500, 12000, 18000, 25000, 55000}


# ---------------- Part A: per-file quality report ----------------
def check_file(path: Path) -> dict:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    month = int(path.stem[-2:])
    revenue = df.units * df.unit_price
    return {
        "file": path.name,
        "rows": len(df),
        "missing_units": int(df.units.isna().sum()),
        "missing_pct": round(df.units.isna().mean() * 100, 3),
        "duplicate_ids": int(df.order_id.duplicated().sum()),
        "bad_prices": int((~df.unit_price.isin(VALID_PRICES)).sum()),
        "wrong_month": int((df.timestamp.dt.month != month).sum()),
        "revenue_cr": round(revenue.sum() / 1e7, 1),
        "avg_order": round(revenue.mean()),
        "top_product": df.groupby("product").units.sum().idxmax(),
    }


# ---------------- Part B: Monte Carlo simulation ----------------
def simulate_refunds(seed: int, prices: np.ndarray, orders_per_month: int = 2_000_000,
                     return_rate: float = 0.02) -> float:
    """One simulated YEAR of refunds (12 months). Big enough to be worth a task."""
    rng = np.random.default_rng(seed)
    total = 0.0
    for _ in range(12):
        returned = rng.random(orders_per_month) < return_rate
        units = rng.integers(1, 6, returned.sum())
        picked = rng.choice(prices, returned.sum())
        total += float((units * picked).sum())
    return total


def main():
    big = ensure_big_data()
    OUT.mkdir(exist_ok=True)
    files = sorted(big.glob("sales_2025-*.csv"))

    print("=" * 60, "\nPART A: data-quality report for 12 files\n" + "=" * 60)
    t = time.perf_counter()
    sequential = [check_file(f) for f in files]
    seq_t = time.perf_counter() - t

    lazy = [dask.delayed(check_file)(f) for f in files]
    t = time.perf_counter()
    threaded = dask.compute(*lazy)                       # threads: pandas releases the GIL a lot
    thr_t = time.perf_counter() - t

    with LocalCluster(n_workers=2, threads_per_worker=1, dashboard_address=":0",
                      silence_logs=logging.ERROR) as cluster, Client(cluster) as client:
        t = time.perf_counter()
        distributed = dask.compute(*lazy)
        dist_t = time.perf_counter() - t

        report = pd.DataFrame(distributed)
        print(report.to_string(index=False))
        report.to_csv(OUT / "file_reports.csv", index=False)
        print(f"\nsequential {seq_t:.2f} s | delayed+threads {thr_t:.2f} s | delayed+cluster {dist_t:.2f} s")
        print("same results:", pd.DataFrame(sequential).equals(pd.DataFrame(threaded)) and
              pd.DataFrame(sequential).equals(report))
        flagged = report[(report.duplicate_ids > 0) | (report.bad_prices > 0) | (report.wrong_month > 0)]
        print("files with integrity problems:", flagged.file.tolist() or "none")
        print("missing-units rate range:", report.missing_pct.min(), "-", report.missing_pct.max(), "%")

        print("\n" + "=" * 60, "\nPART B: Monte Carlo refunds simulation\n" + "=" * 60)
        prices = np.array(sorted(VALID_PRICES))
        remote_prices = client.scatter(prices, broadcast=True)        # sent once
        n_runs = 40
        t = time.perf_counter()
        futures = client.map(simulate_refunds, range(n_runs), prices=remote_prices, pure=False)
        totals = []
        for i, fut in enumerate(as_completed(futures), start=1):
            totals.append(fut.result())
            if i % 10 == 0:
                print(f"  {i}/{n_runs} runs done ({time.perf_counter() - t:.1f} s)")
        sim_t = time.perf_counter() - t

    totals = pd.Series(totals) / 1e7
    totals.to_frame("refunds_crore").to_csv(OUT / "simulation.csv", index=False)
    print(f"\n{n_runs} simulations in {sim_t:.1f} s")
    print(f"yearly refunds (Rs crore): mean {totals.mean():,.1f} | 5th pct {totals.quantile(.05):,.1f} | "
          f"95th pct {totals.quantile(.95):,.1f}")
    print("A planner could budget for the 95th percentile and be safe 19 years out of 20.")

    t = time.perf_counter()
    [simulate_refunds(s, prices) for s in range(n_runs)]
    seq_sim = time.perf_counter() - t
    print(f"same {n_runs} runs sequentially: {seq_sim:.1f} s (cluster: {sim_t:.1f} s)")


if __name__ == "__main__":
    main()
