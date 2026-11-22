"""Lecture 14: Futures (submit / map / as_completed / scatter) and Dask Bag."""
import json
import random
import re
import time
from pathlib import Path
import dask.bag as db
from dask.distributed import Client, LocalCluster, as_completed

HERE = Path(__file__).resolve().parent
COURSE = HERE.parent
OUT = HERE / "output"


def slow_job(i):
    pause = random.uniform(0.1, 1.0)
    time.sleep(pause)
    return i, round(pause, 2)


def price_with_tax(item, table):
    return item, round(table[item] * 1.18, 2)


def make_logs(n=20_000):
    """Write fake JSON-lines logs to output/logs/part-*.jsonl."""
    rng = random.Random(1)
    services = ["auth", "payments", "search", "cart", "profile"]
    (OUT / "logs").mkdir(parents=True, exist_ok=True)
    for part in range(4):
        with open(OUT / "logs" / f"part-{part}.jsonl", "w") as f:
            for i in range(n // 4):
                rec = {"ts": f"2025-06-{rng.randint(1, 30):02d}T{rng.randint(0, 23):02d}:00:00",
                       "service": rng.choice(services),
                       "status": rng.choices(["ok", "error"], weights=[95, 5])[0],
                       "ms": rng.randint(5, 900),
                       "tags": rng.sample(["mobile", "web", "eu", "in", "us", "beta"], k=2)}
                f.write(json.dumps(rec) + "\n")


def main():
    with LocalCluster(n_workers=2, threads_per_worker=2, dashboard_address=":0") as cluster, \
         Client(cluster) as client:
        print("=== 1. submit + result ===")
        f = client.submit(sum, [1, 2, 3])
        print("future:", f)
        print("result:", f.result(), "| status:", f.status)

        print("\n=== 2. map + as_completed (results in finishing order) ===")
        t = time.perf_counter()
        futures = client.map(slow_job, range(8), pure=False)
        for fut in as_completed(futures):
            i, pause = fut.result()
            print(f"  job {i} done after {pause:.2f}s  (elapsed {time.perf_counter() - t:.2f}s)")
        print(f"8 jobs, {sum(fu.result()[1] for fu in futures):.1f}s of work, finished in {time.perf_counter() - t:.2f}s")

        print("\n=== 3. Chaining futures ===")
        a = client.submit(lambda x: x * 10, 4)
        b = client.submit(lambda x: x + 1, a)              # waits for a, on the worker
        print("b =", b.result())

        print("\n=== 4. scatter: send data once ===")
        prices = {"pen": 10, "book": 250, "lamp": 1500, "desk": 12000}
        remote = client.scatter(prices, broadcast=True)
        items = ["pen", "book", "lamp", "desk"] * 25
        out = client.gather(client.map(price_with_tax, items, table=remote))
        print("100 tasks used one scattered dict ->", dict(out))

        print("\n=== 5. Errors come back with the result ===")
        print("(the worker also logs 'Compute Failed' below; that's expected)")
        bad = client.submit(lambda x: 1 / x, 0)
        try:
            bad.result()
        except ZeroDivisionError as e:
            print("status:", bad.status, "| error:", repr(e))

    print("\n=== 6. Dask Bag: word counts across the course READMEs ===")
    readmes = [str(p) for p in COURSE.glob("*/README.md")]
    words = (db.read_text(readmes)
               .map(lambda line: re.findall(r"[a-z]{5,}", line.lower()))
               .flatten())
    print(f"{len(readmes)} files ->", words.frequencies().topk(8, key=lambda kv: kv[1]).compute())

    print("\n=== 7. Dask Bag: JSON-lines logs -> DataFrame ===")
    make_logs()
    records = db.read_text(str(OUT / "logs" / "*.jsonl")).map(json.loads)
    print("first record:", records.take(1)[0])
    errors = records.filter(lambda r: r["status"] == "error")
    print("errors per service:", sorted(errors.pluck("service").frequencies().compute()))
    print("top tags:", records.pluck("tags").flatten().frequencies().topk(3, key=lambda kv: kv[1]).compute())

    slowest = records.foldby("service", lambda acc, r: max(acc, r["ms"]), 0, max, 0).compute()
    print("slowest call per service (foldby):", sorted(slowest))

    ddf = errors.map(lambda r: {k: r[k] for k in ("ts", "service", "ms")}).to_dataframe(
        meta={"ts": "str", "service": "str", "ms": "int64"})
    print("as a Dask DataFrame:", ddf.npartitions, "partitions")
    print(ddf.groupby("service").ms.mean().compute().round(1).sort_values())


if __name__ == "__main__":       # REQUIRED: LocalCluster and Bag use worker processes
    main()
