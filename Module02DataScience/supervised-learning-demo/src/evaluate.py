"""
Step 4 - Evaluate the saved model on the held-out test set (data it never saw).

Run:  python src/evaluate.py
Out:  reports/metrics.txt, reports/confusion_matrix.png, reports/roc_curve.png,
      reports/feature_importance.png
"""
import joblib
import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.inspection import permutation_importance
from sklearn.metrics import (ConfusionMatrixDisplay, RocCurveDisplay, accuracy_score,
                             classification_report, f1_score, precision_score,
                             recall_score, roc_auc_score)

from config import FEATURES, MODEL_PATH, RANDOM_STATE, REPORT_DIR, TARGET, TEST_SET_PATH


def main() -> None:
    bundle = joblib.load(MODEL_PATH)
    model, name = bundle["pipeline"], bundle["name"]
    test = pd.read_csv(TEST_SET_PATH)
    X_test, y_test = test[FEATURES], test[TARGET]

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_prob),
    }
    baseline = max(y_test.mean(), 1 - y_test.mean())  # always-predict-majority

    lines = [f"Model: {name}", f"Test rows: {len(test)}",
             f"Majority-class baseline accuracy: {baseline:.4f}", ""]
    lines += [f"{k:<10} {v:.4f}" for k, v in metrics.items()]
    lines += ["", classification_report(y_test, y_pred,
                                        target_names=["Rejected", "Approved"])]
    report = "\n".join(lines)
    print(report)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    (REPORT_DIR / "metrics.txt").write_text(report)

    # Confusion matrix
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=["Rejected", "Approved"], cmap="Blues", ax=ax)
    ax.set_title("Confusion matrix (test set)")
    fig.tight_layout(); fig.savefig(REPORT_DIR / "confusion_matrix.png", dpi=120); plt.close(fig)

    # ROC curve
    fig, ax = plt.subplots(figsize=(5, 4))
    RocCurveDisplay.from_predictions(y_test, y_prob, name=name, ax=ax)
    ax.plot([0, 1], [0, 1], "--", color="grey", label="Random guess")
    ax.legend(loc="lower right"); ax.set_title("ROC curve (test set)")
    fig.tight_layout(); fig.savefig(REPORT_DIR / "roc_curve.png", dpi=120); plt.close(fig)

    # Permutation feature importance (model-agnostic)
    imp = permutation_importance(model, X_test, y_test, scoring="roc_auc",
                                 n_repeats=10, random_state=RANDOM_STATE)
    order = imp.importances_mean.argsort()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh([FEATURES[i] for i in order], imp.importances_mean[order], color="#3b75af")
    ax.set_xlabel("Drop in ROC-AUC when feature is shuffled")
    ax.set_title("Feature importance")
    fig.tight_layout(); fig.savefig(REPORT_DIR / "feature_importance.png", dpi=120); plt.close(fig)

    print(f"Reports saved in {REPORT_DIR.name}/")


if __name__ == "__main__":
    main()
