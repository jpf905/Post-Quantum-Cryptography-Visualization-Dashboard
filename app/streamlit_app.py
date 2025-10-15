# --- ensure 'src' is importable ---
import sys, os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
print("DEBUG: Project root added to sys.path ->", ROOT_DIR)

# --- regular imports ---
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from src.preprocess import load_data
from src.train_models import train_all
from src.utils import TARGETS, nice_bytes


st.set_page_config(page_title="PQC Visualization Dashboard", layout="wide")
st.title("🔐 PQC Visualization Dashboard")
st.caption("Compare performance, sizes, and security across quantum-resistant schemes — and predict timings with simple ML.")

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "benchmarks.csv"
st.sidebar.header("Data")
csv_path = st.sidebar.text_input("CSV path", value=str(DATA_PATH))
st.sidebar.info("Use the included synthetic CSV or point to your own.")

# Load data
err = None
try:
    df = load_data(csv_path)
except Exception as e:
    err = str(e)
if err:
    st.error(err)
    st.stop()

# Sidebar filters
with st.sidebar:
    st.header("Filters")
    scheme_sel = st.multiselect("Scheme type", sorted(df["scheme"].dropna().unique().tolist()))
    fam_sel = st.multiselect("Family", sorted(df["family"].dropna().unique().tolist()))
    cat_sel = st.multiselect("Category", sorted(df["category"].dropna().unique().tolist()))
    lvl_sel = st.multiselect("Security level", sorted(df["security_level"].dropna().unique().tolist()))
    impl_sel = st.multiselect("Implementation", sorted(df["impl"].dropna().unique().tolist()))

mask = pd.Series(True, index=df.index)
if scheme_sel: mask &= df["scheme"].isin(scheme_sel)
if fam_sel: mask &= df["family"].isin(fam_sel)
if cat_sel: mask &= df["category"].isin(cat_sel)
if lvl_sel: mask &= df["security_level"].isin(lvl_sel)
if impl_sel: mask &= df["impl"].isin(impl_sel)
fdf = df[mask].copy()

tab1, tab2, tab3 = st.tabs(["📊 Explore", "📐 Sizes", "🤖 ML Predictions"])

with tab1:
    st.subheader("Timing trade-offs")
    metric = st.selectbox("Timing metric", TARGETS, index=1)
    size_axis = st.selectbox("Size axis (x)", ["pk_bytes","sk_bytes","ct_or_sig_bytes","security_level"], index=0)
    if fdf.empty:
        st.warning("No rows match your filters.")
    else:
        fig, ax = plt.subplots(figsize=(7,5))
        sns.scatterplot(data=fdf, x=size_axis, y=metric, hue="family", style="scheme", s=90, ax=ax)
        ax.set_xlabel(size_axis)
        ax.set_ylabel(f"{metric} (ms)")
        ax.set_title(f"{metric} vs {size_axis}")
        st.pyplot(fig)

with tab2:
    st.subheader("Key / Secret / Ciphertext-or-Signature sizes")
    cols = st.columns(3)
    for i, col in enumerate(["pk_bytes","sk_bytes","ct_or_sig_bytes"]):
        with cols[i]:
            st.metric(col.replace("_"," ").title(), value=nice_bytes(fdf[col].median()) if not fdf.empty else "—")
    st.dataframe(fdf[["scheme","family","variant","security_level","impl","pk_bytes","sk_bytes","ct_or_sig_bytes"]].reset_index(drop=True))

with tab3:
    st.subheader("Train lightweight regressors to predict timings")
    with st.spinner("Training models..."):
        results = train_all(csv_path)
    if not results:
        st.info("Not enough data to train any model.")
    else:
        for t, res in results.items():
            st.markdown(f"**Target:** `{t}`  |  Samples: `{res.n_samples}`  |  CV RMSE: `{res.cv_rmse_ms:.3f} ms`")
        # Allow ad-hoc predictions
        st.divider()
        st.markdown("### Predict from a hypothetical configuration")
        scheme = st.selectbox("Scheme", sorted(df["scheme"].unique().tolist()))
        family = st.selectbox("Family", sorted(df["family"].unique().tolist()))
        category = st.selectbox("Category", sorted(df["category"].unique().tolist()))
        variant = st.selectbox("Variant", sorted(df["variant"].unique().tolist()))
        impl = st.selectbox("Implementation", sorted(df["impl"].unique().tolist()))
        level = st.number_input("Security level (1-5)", value=3, min_value=1, max_value=5, step=1)
        pk = st.number_input("Public key bytes", value=int(df["pk_bytes"].median()))
        sk = st.number_input("Secret key bytes", value=int(df["sk_bytes"].median()))
        ct = st.number_input("CT/Sig bytes", value=int(df["ct_or_sig_bytes"].median()))
        import pandas as pd
        row = pd.DataFrame([{
            "scheme": scheme, "family": family, "category": category, "variant": variant, "impl": impl,
            "security_level": level, "pk_bytes": pk, "sk_bytes": sk, "ct_or_sig_bytes": ct
        }])
        st.write("Input:", row)
        preds = {}
        for t, res in results.items():
            try:
                preds[t] = float(res.pipeline.predict(row)[0])
            except Exception as e:
                preds[t] = None
        st.markdown("**Predicted timings (ms):**")
        st.json(preds)
        