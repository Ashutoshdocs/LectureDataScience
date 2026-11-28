from pathlib import Path
import logging
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(filename=LOG_DIR / "employee_analytics.log",
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def main():
    sns.set_theme(style="whitegrid", context="notebook")
    df = pd.read_csv(INPUT_DIR / "employees.csv")
    for col in ["salary", "experience_years", "performance_score"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["salary", "experience_years", "department"])

    summary = df.groupby("department", as_index=False).agg(
        employee_count=("employee_id", "count"),
        average_salary=("salary", "mean"),
        median_salary=("salary", "median"),
        average_experience=("experience_years", "mean"),
    )
    summary.to_csv(OUTPUT_DIR / "department_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.histplot(data=df, x="salary", bins=12, kde=True, ax=ax)
    ax.set(title="Employee Salary Distribution", xlabel="Annual salary",
           ylabel="Employee count")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "salary_distribution.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x="department", y="salary", ax=ax)
    ax.set(title="Salary Distribution by Department",
           xlabel="Department", ylabel="Annual salary")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "salary_by_department.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=df, x="experience_years", y="salary",
                    hue="department", ax=ax)
    sns.regplot(data=df, x="experience_years", y="salary",
                scatter=False, color="black", ax=ax)
    ax.set(title="Experience vs Salary", xlabel="Experience (years)",
           ylabel="Annual salary")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "experience_vs_salary.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    numeric = df[["experience_years", "salary", "performance_score"]]
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(numeric.corr(), annot=True, cmap="vlag", center=0,
                fmt=".2f", ax=ax)
    ax.set_title("Employee Metrics Correlation")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "correlation_heatmap.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    logging.info("Employee analysis completed for %s records", len(df))
    print(f"Analyzed {len(df)} employee records. Outputs: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
