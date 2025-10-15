import pandas as pd
from typing import Tuple
from .utils import TARGETS, CAT_FEATS, NUM_FEATS

REQUIRED_COLUMNS = set(TARGETS + CAT_FEATS + NUM_FEATS)

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Standardize column names
    df.columns = [c.strip() for c in df.columns]
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    # Convert to numeric where appropriate
    for c in ["security_level","pk_bytes","sk_bytes","ct_or_sig_bytes"] + TARGETS:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    # Drop fully-empty rows for targets
    if df[TARGETS].isna().all(axis=1).any():
        df = df[~df[TARGETS].isna().all(axis=1)].copy()
    return df

def split_features_targets(df: pd.DataFrame, target: str) -> Tuple[pd.DataFrame, pd.Series]:
    y = df[target].dropna()
    X = df.loc[y.index, CAT_FEATS + NUM_FEATS].copy()
    return X, y
