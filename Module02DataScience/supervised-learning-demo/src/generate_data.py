"""
Step 1 - Generate a synthetic, labeled dataset for supervised learning.

Problem: predict whether a loan application will be APPROVED (1) or REJECTED (0)
from applicant features. Every row has a known label -> that's what makes this
"supervised" learning.

Run:  python src/generate_data.py
Out:  data/loan_data.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

RANDOM_STATE = 42
N_ROWS = 1000

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "loan_data.csv"


def generate(n: int = N_ROWS, seed: int = RANDOM_STATE) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    age = rng.integers(21, 65, n)
    income = rng.normal(60_000, 20_000, n).clip(15_000, 200_000).round(-2)
    loan_amount = rng.normal(150_000, 60_000, n).clip(10_000, 500_000).round(-3)
    credit_score = rng.normal(680, 60, n).clip(300, 850).round()
    years_employed = np.minimum(rng.exponential(6, n), age - 18).round(1)
    existing_debt = rng.normal(15_000, 10_000, n).clip(0, 80_000).round(-2)
    education = rng.choice(["High School", "Bachelor", "Master", "PhD"], n,
                           p=[0.35, 0.40, 0.20, 0.05])
    employment_type = rng.choice(["Salaried", "Self-Employed", "Contract"], n,
                                 p=[0.60, 0.25, 0.15])

    # Hidden "true" rule that generates the label (the model must learn it).
    edu_bonus = pd.Series(education).map(
        {"High School": 0.0, "Bachelor": 0.3, "Master": 0.5, "PhD": 0.6}).to_numpy()
    emp_bonus = pd.Series(employment_type).map(
        {"Salaried": 0.4, "Self-Employed": 0.0, "Contract": -0.3}).to_numpy()

    score = (
        0.025 * (credit_score - 680)
        + 0.00004 * (income - 60_000)
        - 0.000012 * (loan_amount - 150_000)
        - 0.00005 * (existing_debt - 15_000)
        + 0.08 * years_employed
        + edu_bonus + emp_bonus
        - 0.5
    )
    prob = 1 / (1 + np.exp(-score))
    approved = (rng.random(n) < prob).astype(int)

    df = pd.DataFrame({
        "applicant_id": [f"A{i:04d}" for i in range(1, n + 1)],
        "age": age,
        "annual_income": income,
        "loan_amount": loan_amount,
        "credit_score": credit_score.astype(int),
        "years_employed": years_employed,
        "existing_debt": existing_debt,
        "education": education,
        "employment_type": employment_type,
        "approved": approved,
    })

    # Inject a few missing values so the pipeline has to handle real-world mess.
    for col in ["annual_income", "credit_score", "employment_type"]:
        idx = rng.choice(n, size=int(0.02 * n), replace=False)
        df.loc[idx, col] = np.nan

    return df


if __name__ == "__main__":
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df = generate()
    df.to_csv(OUT_PATH, index=False)
    print(f"Saved {len(df)} rows -> {OUT_PATH.relative_to(ROOT)}")
    print(f"Approval rate: {df['approved'].mean():.1%}")
    print(df.head())
