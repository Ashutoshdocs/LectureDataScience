from pathlib import Path
import logging

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "infrastructure_dashboard.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def main():
    # Load monitoring data and parse timestamps.
    df = pd.read_csv(INPUT_DIR / "infrastructure_metrics.csv", parse_dates=["timestamp"])
    df = df.sort_values("timestamp")

    # Produce a daily summary for downstream reporting.
    df["day"] = df["timestamp"].dt.date.astype(str)
    daily = df.groupby("day", as_index=False).agg(
        cpu_avg=("cpu_percent", "mean"),
        memory_avg=("memory_percent", "mean"),
        disk_avg=("disk_percent", "mean"),
        latency_avg=("latency_ms", "mean"),
    )
    daily.to_csv(OUTPUT_DIR / "daily_summary.csv", index=False)

    # Build a four-panel monitoring dashboard.
    fig, axes = plt.subplots(2, 2, figsize=(14, 9), sharex=True)
    metrics = [
        ("cpu_percent", "CPU Utilization", "Percent"),
        ("memory_percent", "Memory Utilization", "Percent"),
        ("disk_percent", "Disk Utilization", "Percent"),
        ("latency_ms", "API Response Latency", "Milliseconds"),
    ]
    for ax, (column, title, ylabel) in zip(axes.flat, metrics):
        for server, server_df in df.groupby("server"):
            ax.plot(server_df["timestamp"], server_df[column],
                    marker="o", markersize=3, linewidth=1.5, label=server)
        ax.set_title(title)
        ax.set_ylabel(ylabel)
        ax.grid(True, alpha=0.25)

    # Mark the CPU warning threshold.
    axes[0, 0].axhline(80, color="red", linestyle="--",
                       linewidth=1.5, label="80% threshold")
    for ax in axes.flat:
        ax.legend(fontsize=8)
    axes[1, 0].set_xlabel("Timestamp")
    axes[1, 1].set_xlabel("Timestamp")
    fig.suptitle("Infrastructure Monitoring Dashboard", fontsize=16)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "infrastructure_dashboard.png",
                dpi=200, bbox_inches="tight")
    fig.savefig(OUTPUT_DIR / "infrastructure_dashboard.pdf",
                bbox_inches="tight")
    plt.close(fig)

    cpu_breaches = int((df["cpu_percent"] > 80).sum())
    logging.info("Dashboard generated. CPU samples above 80%%: %s", cpu_breaches)
    print(f"Dashboard generated. CPU samples above 80%: {cpu_breaches}")
    print(f"Results saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
