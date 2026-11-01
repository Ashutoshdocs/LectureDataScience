"""
Browser UI for the Loan Approval supervised-learning demo.

Run:  streamlit run app.py
Then open the URL it prints (usually http://localhost:8501).

Requires a trained model: run `python src/train.py` (and `python src/evaluate.py`
for the report charts) first, or use the "Train model" button in the sidebar.
"""
import subprocess
import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from config import (CATEGORICAL_FEATURES, DATA_PATH, FEATURES, MODEL_PATH,  # noqa: E402
                    NUMERIC_FEATURES, REPORT_DIR, TARGET)

st.set_page_config(page_title="Loan Approval ML Demo", page_icon="🏦", layout="wide")


# ---------------------------------------------------------------- helpers ---
@st.cache_resource
def load_model(mtime: float):
    """mtime is part of the cache key so a retrained model is picked up."""
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def run_script(name: str) -> tuple[bool, str]:
    result = subprocess.run([sys.executable, str(ROOT / "src" / name)],
                            capture_output=True, text=True, cwd=ROOT)
    return result.returncode == 0, result.stdout + result.stderr


# ---------------------------------------------------------------- sidebar ---
st.sidebar.title("🏦 Loan Approval ML")
st.sidebar.caption("Supervised learning demo · scikit-learn")

if st.sidebar.button("🔄 Train / retrain model", width="stretch"):
    with st.spinner("Generating data, training and evaluating…"):
        for script in ["generate_data.py", "train.py", "evaluate.py"]:
            ok, log = run_script(script)
            if not ok:
                st.sidebar.error(f"{script} failed")
                st.sidebar.code(log[-2000:])
                st.stop()
    load_data.clear()
    st.sidebar.success("Model trained ✔")

if not MODEL_PATH.exists():
    st.title("Loan Approval Prediction")
    st.warning("No trained model found. Click **Train / retrain model** in the sidebar "
               "(or run `python src/train.py`).")
    st.stop()

bundle = load_model(MODEL_PATH.stat().st_mtime)
model, model_name = bundle["pipeline"], bundle["name"]
st.sidebar.markdown(f"**Model in use:** `{model_name}`")
st.sidebar.markdown(
    "**How it works**\n\n"
    "1. Learned from 800 labeled past applications\n"
    "2. Tested on 200 it had never seen\n"
    "3. Now predicts the label for new applicants"
)

st.title("Loan Approval Prediction")
tab_predict, tab_batch, tab_report, tab_data = st.tabs(
    ["🔮 Predict", "📄 Batch predict", "📊 Model report", "🔍 Data explorer"])


# ---------------------------------------------------------------- predict ---
with tab_predict:
    st.subheader("Enter applicant details")
    with st.form("applicant"):
        c1, c2, c3 = st.columns(3)
        with c1:
            age = st.slider("Age", 21, 64, 35)
            years_employed = st.number_input("Years employed", 0.0, 45.0, 5.0, 0.5)
            education = st.selectbox("Education", ["High School", "Bachelor", "Master", "PhD"], 1)
        with c2:
            annual_income = st.number_input("Annual income", 10_000, 300_000, 60_000, 1_000)
            existing_debt = st.number_input("Existing debt", 0, 100_000, 15_000, 1_000)
            employment_type = st.selectbox("Employment type",
                                           ["Salaried", "Self-Employed", "Contract"])
        with c3:
            credit_score = st.slider("Credit score", 300, 850, 680)
            loan_amount = st.number_input("Loan amount", 10_000, 600_000, 150_000, 5_000)
        threshold = st.slider("Decision threshold (approve if probability ≥)", 0.1, 0.9, 0.5, 0.05)
        submitted = st.form_submit_button("Predict", type="primary", width="stretch")

    if submitted:
        row = pd.DataFrame([{
            "age": age, "annual_income": annual_income, "loan_amount": loan_amount,
            "credit_score": credit_score, "years_employed": years_employed,
            "existing_debt": existing_debt, "education": education,
            "employment_type": employment_type,
        }])
        prob = float(model.predict_proba(row[FEATURES])[0, 1])
        approved = prob >= threshold

        r1, r2 = st.columns([1, 2])
        with r1:
            if approved:
                st.success("### ✅ Approved")
            else:
                st.error("### ❌ Rejected")
            st.metric("Approval probability", f"{prob:.1%}")
        with r2:
            st.progress(prob, text=f"Probability {prob:.1%} vs threshold {threshold:.0%}")
            if abs(prob - threshold) < 0.1:
                st.info("Borderline case — the model is not very confident either way.")
            st.caption("Try changing credit score, loan amount or income to see how the "
                       "prediction responds.")


# ------------------------------------------------------------------ batch ---
with tab_batch:
    st.subheader("Predict many applicants from a CSV")
    st.caption(f"Required columns: {', '.join(FEATURES)}")

    sample = ROOT / "data" / "new_applicants.csv"
    if sample.exists():
        st.download_button("Download sample CSV", sample.read_bytes(),
                           "new_applicants.csv", "text/csv")

    upload = st.file_uploader("Upload CSV", type="csv")
    if upload is not None:
        new = pd.read_csv(upload)
        missing = sorted(set(FEATURES) - set(new.columns))
        if missing:
            st.error(f"Missing columns: {missing}")
        else:
            out = new.copy()
            out["approval_probability"] = model.predict_proba(new[FEATURES])[:, 1].round(3)
            out["prediction"] = out["approval_probability"].map(
                lambda p: "Approved" if p >= 0.5 else "Rejected")
            m1, m2 = st.columns(2)
            m1.metric("Applicants", len(out))
            m2.metric("Predicted approved", f"{(out['prediction'] == 'Approved').mean():.0%}")
            st.dataframe(out, width="stretch", hide_index=True)
            st.download_button("Download predictions", out.to_csv(index=False).encode(),
                               "predictions.csv", "text/csv", type="primary")


# ----------------------------------------------------------------- report ---
with tab_report:
    st.subheader("How good is the model? (held-out test set)")
    metrics_file = REPORT_DIR / "metrics.txt"
    if not metrics_file.exists():
        st.warning("No report yet — run `python src/evaluate.py` or click Train in the sidebar.")
    else:
        text = metrics_file.read_text()
        scores = {}
        for line in text.splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[0] in {"accuracy", "precision", "recall", "f1", "roc_auc"}:
                scores[parts[0]] = float(parts[1])
        if scores:
            cols = st.columns(len(scores))
            for col, (k, v) in zip(cols, scores.items()):
                col.metric(k.replace("_", "-").upper() if k == "roc_auc" else k.title(), f"{v:.3f}")

        i1, i2, i3 = st.columns(3)
        for col, (fname, title) in zip(
                [i1, i2, i3],
                [("confusion_matrix.png", "Confusion matrix"),
                 ("roc_curve.png", "ROC curve"),
                 ("feature_importance.png", "Feature importance")]):
            path = REPORT_DIR / fname
            if path.exists():
                col.image(str(path), caption=title, width="stretch")

        with st.expander("Full classification report"):
            st.code(text)


# ------------------------------------------------------------------- data ---
with tab_data:
    st.subheader("Training data")
    df = load_data()
    d1, d2, d3 = st.columns(3)
    d1.metric("Rows", len(df))
    d2.metric("Features", len(FEATURES))
    d3.metric("Approval rate", f"{df[TARGET].mean():.0%}")

    st.dataframe(df.head(100), width="stretch", hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        feat = st.selectbox("Numeric feature: average by outcome", NUMERIC_FEATURES, index=3)
        avg = df.groupby(TARGET)[feat].mean().rename({0: "Rejected", 1: "Approved"})
        st.bar_chart(avg)
    with c2:
        cat = st.selectbox("Category: approval rate", CATEGORICAL_FEATURES)
        st.bar_chart(df.groupby(cat)[TARGET].mean().sort_values(ascending=False))

    with st.expander("Missing values per column"):
        st.dataframe(df.isna().sum().rename("missing"), width="stretch")
