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

logging.basicConfig(filename=LOG_DIR / "student_performance.log",
                    level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")

def main():
    sns.set_theme(style="ticks", context="notebook")
    df = pd.read_csv(INPUT_DIR / "students.csv")
    numeric_cols = ["study_hours", "attendance_percent",
                    "assignments_completed", "sleep_hours", "marks"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=numeric_cols + ["course"])

    summary = df.groupby("course", as_index=False).agg(
        student_count=("student_id", "count"),
        average_marks=("marks", "mean"),
        median_marks=("marks", "median"),
        average_study_hours=("study_hours", "mean"),
        average_attendance=("attendance_percent", "mean"),
    )
    summary.to_csv(OUTPUT_DIR / "course_summary.csv", index=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.scatterplot(data=df, x="study_hours", y="marks",
                    hue="course", style="course", s=75, ax=ax)
    ax.set(title="Study Hours vs Student Marks",
           xlabel="Study hours per day", ylabel="Marks")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "study_hours_vs_marks.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.violinplot(data=df, x="course", y="marks", inner="quart", ax=ax)
    ax.set(title="Marks Distribution by Course", xlabel="Course", ylabel="Marks")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "marks_by_course.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    pair_grid = sns.pairplot(
        df, vars=["study_hours", "attendance_percent", "sleep_hours", "marks"],
        hue="course", corner=True, diag_kind="hist"
    )
    pair_grid.figure.suptitle("Student Performance Pair Plot", y=1.02)
    pair_grid.savefig(OUTPUT_DIR / "student_pairplot.png", dpi=160, bbox_inches="tight")
    plt.close(pair_grid.figure)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm",
                center=0, fmt=".2f", ax=ax)
    ax.set_title("Student Metrics Correlation")
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "student_correlation_heatmap.png",
                dpi=180, bbox_inches="tight")
    plt.close(fig)

    logging.info("Student analysis completed for %s records", len(df))
    print(f"Analyzed {len(df)} student records. Outputs: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
