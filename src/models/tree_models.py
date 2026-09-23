import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
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
    model: RandomForestClassifier | XGBClassifier,
    features: pd.DataFrame,
) -> pd.Series:
    X = prepare_model_inputs(features)

    probabilities = model.predict_proba(X)[:, 1]

    return pd.Series(
        probabilities,
        index=features.index,
        name="fraud_probability",
    )

def train_gradient_boosting(
    train_features: pd.DataFrame,
) -> XGBClassifier:
    X_train = prepare_model_inputs(train_features)
    y_train = train_features["is_fraud"]

    negative_count = (y_train == 0).sum()
    positive_count = (y_train == 1).sum()

    scale_pos_weight = (
        negative_count / positive_count
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=3,
        learning_rate=0.1,
        scale_pos_weight=scale_pos_weight,
        random_state=42,
        n_jobs=-1,
        eval_metric="logloss",
    )

    model.fit(X_train, y_train)

    return model