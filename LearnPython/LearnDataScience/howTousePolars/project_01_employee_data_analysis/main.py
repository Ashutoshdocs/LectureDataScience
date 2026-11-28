from pathlib import Path
import polars as pl

from analysis import clean_employees, join_departments, department_summary

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "output"

EMPLOYEES_FILE = INPUT_DIR / "employees.csv"
DEPARTMENTS_FILE = INPUT_DIR / "departments.csv"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    employees = pl.read_csv(EMPLOYEES_FILE)
    departments = pl.read_csv(DEPARTMENTS_FILE)

    print("Original employee schema:")
    print(employees.schema)

    print("\nNull counts before cleaning:")
    print(employees.null_count())

    cleaned = clean_employees(employees)
    enriched = join_departments(cleaned, departments)
    summary = department_summary(enriched)

    print("\nCleaned and enriched employees:")
    print(enriched)

    print("\nDepartment summary:")
    print(summary)

    enriched.write_csv(OUTPUT_DIR / "cleaned_employees.csv")
    summary.write_csv(OUTPUT_DIR / "department_summary.csv")
    enriched.write_parquet(OUTPUT_DIR / "cleaned_employees.parquet")

    print("\nReports saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    main()
