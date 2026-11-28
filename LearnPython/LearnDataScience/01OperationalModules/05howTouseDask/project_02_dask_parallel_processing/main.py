import csv
import logging
from pathlib import Path

from dask import compute
from dask.distributed import Client, LocalCluster

from tasks import square, cube, summarize

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "input" / "numbers.txt"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"


def configure_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_DIR / "parallel_processing.log",
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def load_numbers():
    numbers = []
    for line_number, line in enumerate(INPUT_FILE.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            numbers.append(int(stripped))
        except ValueError as error:
            raise ValueError(f"Invalid integer on line {line_number}: {stripped}") from error
    return numbers


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    configure_logging()

    numbers = load_numbers()
    if not numbers:
        raise ValueError("No numbers found in input file.")

    cluster = LocalCluster(
        n_workers=2,
        threads_per_worker=1,
        processes=True,
        dashboard_address=":8787",
    )
    client = Client(cluster)

    try:
        print("Dask dashboard:", client.dashboard_link)

        square_tasks = [square(number) for number in numbers]
        cube_tasks = [cube(number) for number in numbers]

        # Compute related delayed tasks together.
        squares, cubes = compute(square_tasks, cube_tasks)

        summary_task = summarize(squares)
        summary = summary_task.compute()

        output_file = OUTPUT_DIR / "parallel_results.csv"
        with output_file.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["number", "square", "cube"],
            )
            writer.writeheader()
            for number, squared, cubed in zip(numbers, squares, cubes):
                writer.writerow({
                    "number": number,
                    "square": squared,
                    "cube": cubed,
                })

        logging.info("Processed %d numbers", len(numbers))
        logging.info("Summary: %s", summary)

        print("\nSummary:", summary)
        print("Results saved to:", output_file)
        print("Keep the dashboard open while the cluster is running.")
    finally:
        client.close()
        cluster.close()


if __name__ == "__main__":
    main()
