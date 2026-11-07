"""
CSV Playground — upload a CSV, explore it, run Python (pandas + numpy + file I/O)
against it, see the output live, and download the results.

Run:
    pip install "streamlit>=1.50" pandas numpy
    streamlit run app.py
"""

import contextlib
import io
import os
import tempfile
import time
import traceback

import numpy as np
import pandas as pd
import streamlit as st

# ─────────────────────────────────────────────────────────────
# Page config + styling
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CSV Playground",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: radial-gradient(circle at 10% 0%, #1e1b4b 0%, #0f172a 45%, #020617 100%);
        color: #e2e8f0;
    }

    .hero {
        padding: 1.6rem 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(99,102,241,.25), rgba(236,72,153,.18));
        border: 1px solid rgba(255,255,255,.08);
        box-shadow: 0 10px 40px rgba(0,0,0,.35);
        margin-bottom: 1.4rem;
    }
    .hero h1 {
        margin: 0; font-weight: 800; font-size: 2.3rem;
        background: linear-gradient(90deg, #a5b4fc, #f0abfc, #fda4af);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .hero p { margin: .4rem 0 0; color: #cbd5e1; font-size: 1.02rem; }

    .card {
        padding: 1rem 1.2rem; border-radius: 16px;
        background: rgba(255,255,255,.04);
        border: 1px solid rgba(255,255,255,.08);
        backdrop-filter: blur(6px);
    }
    .metric-label { color: #94a3b8; font-size: .8rem; text-transform: uppercase; letter-spacing: .08em; }
    .metric-value { color: #f8fafc; font-size: 1.6rem; font-weight: 800; }

    .section-title {
        font-weight: 700; font-size: 1.15rem; margin: 1.2rem 0 .6rem;
        color: #e0e7ff; display: flex; align-items: center; gap: .5rem;
    }

    textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.9rem !important;
        background: #0b1020 !important;
        color: #e2e8f0 !important;
        border-radius: 12px !important;
    }

    .console {
        font-family: 'JetBrains Mono', monospace;
        background: #050816; color: #a7f3d0;
        border: 1px solid rgba(167,243,208,.18);
        border-radius: 12px; padding: 1rem 1.2rem;
        white-space: pre-wrap; max-height: 420px; overflow: auto;
        font-size: .88rem;
    }
    .console.error { color: #fecaca; border-color: rgba(254,202,202,.25); }

    .stButton > button, .stDownloadButton > button {
        border-radius: 12px; font-weight: 600; border: none;
        background: linear-gradient(135deg, #6366f1, #ec4899);
        color: white; padding: .55rem 1.2rem;
        transition: transform .08s ease, box-shadow .2s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px rgba(236,72,153,.35);
        color: white;
    }

    [data-testid="stSidebar"] {
        background: rgba(2,6,23,.85);
        border-right: 1px solid rgba(255,255,255,.06);
    }
    [data-testid="stFileUploader"] section {
        border-radius: 14px; border: 1.5px dashed rgba(165,180,252,.45);
        background: rgba(99,102,241,.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────────────────────
# Session state
# ─────────────────────────────────────────────────────────────
ss = st.session_state
ss.setdefault("df", None)               # working DataFrame (can be modified by code)
ss.setdefault("original_df", None)      # untouched copy of upload
ss.setdefault("file_name", None)
ss.setdefault("stdout", "")
ss.setdefault("error", "")
ss.setdefault("result", None)
ss.setdefault("exec_time", None)
ss.setdefault("history", [])
ss.setdefault("workdir", tempfile.mkdtemp(prefix="csv_playground_"))
ss.setdefault("editor", "# df is your data. Try:\nprint(df.head())\nresult = df.describe()")


def set_editor(text):
    ss.editor = text

WORKDIR = ss.workdir

# ─────────────────────────────────────────────────────────────
# Example snippets
# ─────────────────────────────────────────────────────────────
SNIPPETS = {
    "👋 Quick overview": """print("Shape:", df.shape)
print("\\nColumns:", list(df.columns))
print("\\nMissing values per column:")
print(df.isna().sum())
result = df.describe(include="all").T""",

    "🔢 NumPy stats on numeric columns": """num = df.select_dtypes(include=np.number)
arr = num.to_numpy()
print("Mean :", np.round(np.nanmean(arr, axis=0), 3))
print("Std  :", np.round(np.nanstd(arr, axis=0), 3))
print("Min  :", np.nanmin(arr, axis=0))
print("Max  :", np.nanmax(arr, axis=0))
result = pd.DataFrame({
    "mean": np.nanmean(arr, axis=0),
    "median": np.nanmedian(arr, axis=0),
    "std": np.nanstd(arr, axis=0),
}, index=num.columns)""",

    "🧹 Clean data (drop dupes / fill NaN)": """before = len(df)
df = df.drop_duplicates()
for c in df.select_dtypes(include=np.number).columns:
    df[c] = df[c].fillna(df[c].median())
df = df.fillna("Unknown")
print(f"Removed {before - len(df)} duplicate rows")
print("Remaining NaNs:", int(df.isna().sum().sum()))
result = df""",

    "📊 Group & aggregate": """# Groups by the first text column, aggregates numeric columns
cat_cols = df.select_dtypes(exclude=np.number).columns
num_cols = df.select_dtypes(include=np.number).columns
if len(cat_cols) and len(num_cols):
    result = df.groupby(cat_cols[0])[list(num_cols)].agg(["mean", "sum", "count"])
    print(f"Grouped by '{cat_cols[0]}'")
else:
    print("Need at least one text and one numeric column.")""",

    "📁 File handling (write / read / list)": """# Save a filtered copy, read it back, and write a text report
path = os.path.join(WORKDIR, "top_rows.csv")
df.head(20).to_csv(path, index=False)

with open(os.path.join(WORKDIR, "report.txt"), "w") as f:
    f.write(f"Rows: {len(df)}\\nCols: {df.shape[1]}\\n")
    f.write("Columns: " + ", ".join(map(str, df.columns)))

print("Files in workspace:", os.listdir(WORKDIR))
with open(os.path.join(WORKDIR, "report.txt")) as f:
    print(f.read())

result = pd.read_csv(path)""",

    "🔍 Filter rows": """# Rows where the first numeric column is above its mean
num_cols = df.select_dtypes(include=np.number).columns
col = num_cols[0]
result = df[df[col] > df[col].mean()]
print(f"{len(result)} rows where {col} > mean ({df[col].mean():.2f})")""",
}

# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────
def metric_card(label, value):
    st.markdown(
        f'<div class="card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


def run_user_code(code: str):
    """Execute user code with df / pd / np / os available; capture stdout."""
    namespace = {
        "pd": pd, "np": np, "os": os, "io": io,
        "df": ss.df.copy(),
        "original_df": ss.original_df.copy(),
        "WORKDIR": WORKDIR,
        "result": None,
    }
    buf = io.StringIO()
    start = time.perf_counter()
    cwd = os.getcwd()
    try:
        os.chdir(WORKDIR)  # relative file paths land in the workspace
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(compile(code, "<your code>", "exec"), namespace)
        ss.error = ""
        # keep df changes if user reassigned/modified it
        if isinstance(namespace.get("df"), pd.DataFrame):
            ss.df = namespace["df"]
        ss.result = namespace.get("result")
    except Exception:
        ss.error = traceback.format_exc()
        ss.result = None
    finally:
        os.chdir(cwd)
    ss.stdout = buf.getvalue()
    ss.exec_time = time.perf_counter() - start
    ss.history.insert(0, {"code": code, "ok": not ss.error, "time": time.strftime("%H:%M:%S")})
    ss.history = ss.history[:15]


def to_csv_bytes(obj) -> bytes:
    if isinstance(obj, pd.Series):
        obj = obj.to_frame()
    return obj.to_csv(index=not isinstance(obj.index, pd.RangeIndex)).encode("utf-8")


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📂 Upload CSV")
    uploaded = st.file_uploader("Drop a .csv file", type=["csv"], label_visibility="collapsed")

    with st.expander("⚙️ Read options"):
        sep = st.selectbox("Delimiter", [",", ";", "\\t", "|"], index=0)
        encoding = st.selectbox("Encoding", ["utf-8", "latin-1", "utf-16"], index=0)
        header = st.checkbox("First row is header", value=True)

    if uploaded is not None and (uploaded.name != ss.file_name or st.button("🔄 Reload file")):
        try:
            real_sep = "\t" if sep == "\\t" else sep
            df = pd.read_csv(uploaded, sep=real_sep, encoding=encoding,
                             header=0 if header else None)
            ss.df, ss.original_df, ss.file_name = df, df.copy(), uploaded.name
            ss.stdout, ss.error, ss.result = "", "", None
            # also store the raw file in the workspace for file-handling demos
            uploaded.seek(0)
            with open(os.path.join(WORKDIR, uploaded.name), "wb") as f:
                f.write(uploaded.read())
            st.success(f"Loaded **{uploaded.name}**")
        except Exception as e:
            st.error(f"Could not read file: {e}")

    if ss.df is not None:
        st.markdown("---")
        st.markdown("## 🧩 Snippets")
        choice = st.selectbox("Insert an example", ["—"] + list(SNIPPETS.keys()))
        st.button("Use snippet", width="stretch",
                  disabled=choice == "—",
                  on_click=set_editor, args=(SNIPPETS.get(choice, ""),))

        st.markdown("---")
        if st.button("↩️ Reset data to original", width="stretch"):
            ss.df = ss.original_df.copy()
            ss.stdout, ss.error, ss.result = "", "", None
            st.rerun()

    st.markdown("---")
    st.caption(
        "Available in your code: `df`, `original_df`, `pd`, `np`, `os`, `io`, `WORKDIR`.\n\n"
        "Assign to `result` to show a table/value and enable its download."
    )

# ─────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
      <h1>🧪 CSV Playground</h1>
      <p>Upload a CSV, explore it, and run live Python with <b>pandas</b>, <b>NumPy</b> and file handling — then download what you made.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if ss.df is None:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><h4>1 · Upload</h4>Drop a CSV in the sidebar.</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><h4>2 · Code</h4>Write pandas / NumPy / file I/O against <code>df</code>.</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><h4>3 · Download</h4>Grab the result, the console output, or saved files.</div>', unsafe_allow_html=True)
    st.stop()

df = ss.df

# ── Metrics
m1, m2, m3, m4 = st.columns(4)
with m1: metric_card("File", ss.file_name if len(ss.file_name) < 22 else ss.file_name[:19] + "…")
with m2: metric_card("Rows", f"{df.shape[0]:,}")
with m3: metric_card("Columns", f"{df.shape[1]:,}")
with m4: metric_card("Missing cells", f"{int(df.isna().sum().sum()):,}")

# ── Data views
st.markdown('<div class="section-title">📋 Your data</div>', unsafe_allow_html=True)
tab_data, tab_info, tab_stats = st.tabs(["Table", "Column info", "Statistics"])
with tab_data:
    max_rows = min(len(df), 1000)
    if max_rows > 5:
        n = st.slider("Rows to show", 5, max_rows, min(50, max_rows))
    else:
        n = max_rows
    st.dataframe(df.head(n), width="stretch", height=360)
with tab_info:
    info = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "non-null": df.notna().sum(),
        "nulls": df.isna().sum(),
        "unique": df.nunique(),
        "sample": [str(df[c].dropna().iloc[0]) if df[c].notna().any() else "" for c in df.columns],
    })
    st.dataframe(info, width="stretch")
with tab_stats:
    try:
        st.dataframe(df.describe(include="all").T.astype(str).replace("nan", ""), width="stretch")
    except ValueError:
        st.info("No statistics available for this data.")

# ── Code editor
st.markdown('<div class="section-title">🐍 Run Python</div>', unsafe_allow_html=True)
code = st.text_area("code", height=260, label_visibility="collapsed", key="editor")

b1, b2, _ = st.columns([1, 1, 4])
run = b1.button("▶ Run code", width="stretch")
if b2.button("🧹 Clear output", width="stretch"):
    ss.stdout, ss.error, ss.result, ss.exec_time = "", "", None, None
    st.rerun()

if run:
    with st.spinner("Running…"):
        run_user_code(code)

# ── Output
if ss.exec_time is not None or ss.stdout or ss.error:
    st.markdown('<div class="section-title">📤 Output</div>', unsafe_allow_html=True)
    if ss.exec_time is not None:
        status = "❌ Error" if ss.error else "✅ Success"
        st.caption(f"{status} · ran in {ss.exec_time*1000:.1f} ms")

    console_text = ss.stdout + (("\n" if ss.stdout else "") + ss.error if ss.error else "")
    if console_text.strip():
        cls = "console error" if ss.error else "console"
        safe = console_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        st.markdown(f'<div class="{cls}">{safe}</div>', unsafe_allow_html=True)

    res = ss.result
    if res is not None:
        st.markdown("**`result`**")
        if isinstance(res, (pd.DataFrame, pd.Series)):
            st.dataframe(res, width="stretch")
        elif isinstance(res, np.ndarray):
            st.dataframe(pd.DataFrame(res), width="stretch")
        else:
            st.code(repr(res))

    # ── Downloads
    st.markdown('<div class="section-title">⬇️ Downloads</div>', unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    base = os.path.splitext(ss.file_name)[0]

    with d1:
        if isinstance(res, (pd.DataFrame, pd.Series)):
            st.download_button("Result (.csv)", to_csv_bytes(res),
                               f"{base}_result.csv", "text/csv", width="stretch")
        elif isinstance(res, np.ndarray):
            st.download_button("Result (.csv)", to_csv_bytes(pd.DataFrame(res)),
                               f"{base}_result.csv", "text/csv", width="stretch")
        elif res is not None:
            st.download_button("Result (.txt)", repr(res).encode(),
                               f"{base}_result.txt", "text/plain", width="stretch")
        else:
            st.caption("Assign to `result` to download it.")
    with d2:
        st.download_button("Console output (.txt)", console_text.encode("utf-8"),
                           f"{base}_output.txt", "text/plain", width="stretch")
    with d3:
        st.download_button("Current df (.csv)", to_csv_bytes(ss.df),
                           f"{base}_modified.csv", "text/csv", width="stretch")

# ── Workspace files (from file-handling code)
files = sorted(f for f in os.listdir(WORKDIR) if os.path.isfile(os.path.join(WORKDIR, f)))
if files:
    with st.expander(f"🗂️ Workspace files ({len(files)}) — files your code created"):
        for fname in files:
            fpath = os.path.join(WORKDIR, fname)
            c1, c2 = st.columns([4, 1])
            c1.markdown(f"`{fname}` · {os.path.getsize(fpath):,} bytes")
            with open(fpath, "rb") as fh:
                c2.download_button("Download", fh.read(), fname, key=f"dl_{fname}",
                                   width="stretch")

# ── History
if ss.history:
    with st.expander("🕘 Run history"):
        for i, h in enumerate(ss.history):
            icon = "✅" if h["ok"] else "❌"
            st.markdown(f"{icon} **{h['time']}**")
            st.code(h["code"], language="python")
            st.button("Load into editor", key=f"hist_{i}",
                      on_click=set_editor, args=(h["code"],))
