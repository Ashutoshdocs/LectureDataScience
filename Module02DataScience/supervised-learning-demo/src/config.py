"""Shared settings used by every script."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "loan_data.csv"
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"
MODEL_PATH = MODEL_DIR / "best_model.joblib"
TEST_SET_PATH = MODEL_DIR / "test_set.csv"

TARGET = "approved"
ID_COL = "applicant_id"

NUMERIC_FEATURES = [
    "age", "annual_income", "loan_amount", "credit_score",
    "years_employed", "existing_debt",
]
CATEGORICAL_FEATURES = ["education", "employment_type"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

TEST_SIZE = 0.2
RANDOM_STATE = 42
