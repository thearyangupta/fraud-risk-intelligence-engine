import pandas as pd
from sklearn.ensemble import RandomForestClassifier

from src.models.logistic_regression import (
    prepare_model_inputs,
)


def train_random_forest(
    train_features: pd.DataFrame,
) -> RandomForestClassifier:
    X_train = prepare_model_inputs(train_features)
    y_train = train_features["is_fraud"]

    model = RandomForestClassifier(
        n_estimators=200,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(X_train, y_train)

    return model


def predict_tree_probabilities(
    model: RandomForestClassifier,
    features: pd.DataFrame,
) -> pd.Series:
    X = prepare_model_inputs(features)

    probabilities = model.predict_proba(X)[:, 1]

    return pd.Series(
        probabilities,
        index=features.index,
        name="fraud_probability",
    )