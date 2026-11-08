import os
import json
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, average_precision_score

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = ROOT_DIR / "data" / "smb_leads.csv"
MODEL_DIR = ROOT_DIR / "models"
MODEL_PATH = MODEL_DIR / "propensity.joblib"
METRICS_PATH = MODEL_DIR / "metrics.json"

def count_products_of_interest(val):
    if pd.isna(val) or not str(val).strip():
        return 0
    return len([x for x in str(val).split(";") if x.strip()])

def train():
    os.makedirs(MODEL_DIR, exist_ok=True)
    df = pd.read_csv(DATA_PATH)
    
    # Target
    y = (df["outcome"] == "Activated").astype(int)
    base_rate = float(y.mean())
    print(f"Total leads: {len(df)}, Activated: {y.sum()} ({base_rate*100:.2f}%)")

    # Feature engineering without leakage
    df["num_products_interest"] = df["products_of_interest"].apply(count_products_of_interest)
    df["employee_count"] = df["employee_count"].fillna(1)
    df["num_sites"] = df["num_sites"].fillna(1)
    df["monthly_telecom_spend_inr"] = df["monthly_telecom_spend_inr"].fillna(df["monthly_telecom_spend_inr"].median())
    
    categorical_cols = [
        "segment", "business_type", "city_tier", "lead_source",
        "preferred_language", "annual_turnover_band", "has_gstin",
        "has_udyam", "current_internet"
    ]
    numeric_cols = [
        "employee_count", "num_sites", "monthly_telecom_spend_inr", "num_products_interest"
    ]

    for col in categorical_cols:
        df[col] = df[col].fillna("Missing").astype(str)

    X = df[categorical_cols + numeric_cols]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), categorical_cols),
            ("num", StandardScaler(), numeric_cols)
        ]
    )

    clf = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.08,
        max_depth=3,
        random_state=42
    )

    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("classifier", clf)
    ])

    pipeline.fit(X_train, y_train)

    # Evaluation
    y_pred_proba = pipeline.predict_proba(X_test)[:, 1]
    roc_auc = float(roc_auc_score(y_test, y_pred_proba))
    pr_auc = float(average_precision_score(y_test, y_pred_proba))

    # Top decile lift & precision@top-20%
    test_eval = pd.DataFrame({"true": y_test.values, "proba": y_pred_proba})
    test_eval = test_eval.sort_values(by="proba", ascending=False).reset_index(drop=True)

    n_top20 = int(len(test_eval) * 0.20)
    precision_top_20 = float(test_eval.iloc[:n_top20]["true"].mean())

    n_top10 = int(len(test_eval) * 0.10)
    top10_rate = float(test_eval.iloc[:n_top10]["true"].mean())
    lift_top_decile = float(top10_rate / base_rate) if base_rate > 0 else 1.0

    print(f"ROC-AUC: {roc_auc:.4f}")
    print(f"PR-AUC:  {pr_auc:.4f}")
    print(f"Precision@top-20%: {precision_top_20*100:.2f}% (vs base rate {base_rate*100:.2f}%)")
    print(f"Lift in top decile: {lift_top_decile:.2f}x")

    # Feature importance
    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    importances = pipeline.named_steps["classifier"].feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    top_factors = [
        {"feature": str(feature_names[i]), "importance": float(importances[i])}
        for i in sorted_idx[:10]
    ]

    metrics = {
        "model_type": "GradientBoostingClassifier",
        "sample_size": len(df),
        "test_size": len(X_test),
        "base_activation_rate": round(base_rate, 4),
        "roc_auc": round(roc_auc, 4),
        "pr_auc": round(pr_auc, 4),
        "precision_at_top_20_pct": round(precision_top_20, 4),
        "lift_top_decile": round(lift_top_decile, 2),
        "top_predictive_factors": top_factors
    }

    joblib.dump(pipeline, MODEL_PATH)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Model saved to: {MODEL_PATH}")
    print(f"Metrics saved to: {METRICS_PATH}")

if __name__ == "__main__":
    train()
