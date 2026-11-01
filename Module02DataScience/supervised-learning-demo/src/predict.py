"""
Step 5 - Use the trained model to predict on NEW, unlabeled applicants.

Run:  python src/predict.py                          # uses data/new_applicants.csv
      python src/predict.py path/to/your_file.csv    # your own file
Out:  data/predictions.csv
"""
import sys
from pathlib import Path

import joblib
import pandas as pd

from config import FEATURES, ID_COL, MODEL_PATH, ROOT


def main() -> None:
    in_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "data" / "new_applicants.csv"
    new = pd.read_csv(in_path)

    missing = set(FEATURES) - set(new.columns)
    if missing:
        sys.exit(f"Input file is missing columns: {sorted(missing)}")

    model = joblib.load(MODEL_PATH)["pipeline"]
    prob = model.predict_proba(new[FEATURES])[:, 1]

    out = new.copy()
    out["approval_probability"] = prob.round(3)
    out["prediction"] = ["Approved" if p >= 0.5 else "Rejected" for p in prob]

    out_path = ROOT / "data" / "predictions.csv"
    out.to_csv(out_path, index=False)

    cols = [c for c in [ID_COL, "credit_score", "annual_income", "loan_amount"] if c in out]
    print(out[cols + ["approval_probability", "prediction"]].to_string(index=False))
    print(f"\nSaved -> {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
