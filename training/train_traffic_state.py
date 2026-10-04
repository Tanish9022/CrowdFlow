"""
Traffic State Tabular Classifier Training Script.
Trains a Random Forest classifier on extracted traffic kinematic features.
Academic Prototype - SPPU CS-331-FP
"""

import argparse
import os
import pandas as pd
from pathlib import Path


def train_classifier(features_csv: str, model_out: str):
    print("=== Crowd Flow: Training Traffic State Classifier ===")
    print(f"Reading dataset: {features_csv}")

    if not os.path.exists(features_csv):
        print(f"[ERROR] Features CSV file not found at: {features_csv}")
        return

    df = pd.read_csv(features_csv)
    print(f"Loaded {len(df)} samples.")
    print("Columns:", list(df.columns))

    feature_cols = [
        "vehicle_count",
        "avg_speed_kmh",
        "occupancy_ratio",
        "stationary_ratio",
        "queue_persistence_s",
        "pedestrian_count"
    ]
    target_col = "ground_truth_state"

    for col in feature_cols + [target_col]:
        if col not in df.columns:
            print(f"[ERROR] Missing required column: {col}")
            return

    X = df[feature_cols]
    y = df[target_col]

    try:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import StratifiedKFold, cross_val_score
        import joblib

        clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42, class_weight="balanced")
        
        min_class_samples = y.value_counts().min()
        if min_class_samples >= 2:
            n_splits = min(5, min_class_samples)
            cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
            scores = cross_val_score(clf, X, y, cv=cv, scoring="accuracy")
            print(f"Cross-Validation Accuracy ({n_splits}-fold): {scores.mean():.4f} (+/- {scores.std():.4f})")
        else:
            print(f"[INFO] Skipping cross-validation: smallest class has {min_class_samples} sample(s). Fitting on full dataset.")

        clf.fit(X, y)
        os.makedirs(os.path.dirname(model_out), exist_ok=True)
        joblib.dump(clf, model_out)
        print(f"Trained Random Forest model saved to: {model_out}")
    except ImportError:
        print("[WARNING] 'scikit-learn' or 'joblib' not installed. Install via: pip install scikit-learn joblib")
    except Exception as e:
        print(f"[ERROR] Failed during training: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Traffic State Classifier")
    parser.add_argument("--features", type=str, default="dataset/traffic_state/labels.csv")
    parser.add_argument("--model_out", type=str, default="models/traffic_rf_classifier.joblib")
    args = parser.parse_args()

    train_classifier(args.features, args.model_out)
