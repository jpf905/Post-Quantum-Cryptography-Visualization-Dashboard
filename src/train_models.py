from dataclasses import dataclass
from typing import Dict, Tuple
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score, KFold
from .preprocess import load_data, split_features_targets
from .utils import TARGETS, CAT_FEATS, NUM_FEATS

N_ESTIMATORS = 200
RANDOM_STATE = 7

@dataclass
class ModelResult:
    pipeline: Pipeline
    cv_rmse_ms: float
    n_samples: int

def build_preprocessor() -> ColumnTransformer:
    cat = Pipeline([
        ("impute", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])
    num = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ])
    return ColumnTransformer([
        ("cat", cat, CAT_FEATS),
        ("num", num, NUM_FEATS),
    ])

def train_all(csv_path: str) -> Dict[str, ModelResult]:
    df = load_data(csv_path)
    results: Dict[str, ModelResult] = {}
    for target in TARGETS:
        X, y = split_features_targets(df, target)
        if len(y) < 4:
            continue  # not enough samples
        pre = build_preprocessor()
        model = RandomForestRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
        pipe = Pipeline([("pre", pre), ("model", model)])
        cv = KFold(n_splits=min(5, len(y)), shuffle=True, random_state=RANDOM_STATE)
        scores = -cross_val_score(pipe, X, y, scoring="neg_root_mean_squared_error", cv=cv)
        pipe.fit(X, y)
        results[target] = ModelResult(pipeline=pipe, cv_rmse_ms=float(scores.mean()), n_samples=len(y))
    return results
