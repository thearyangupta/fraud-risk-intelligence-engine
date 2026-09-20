import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "txn_count_10m_before",
    "txn_count_1h_before",
    "txn_count_24h_before",
    "seconds_since_prev_txn",
    "prior_txn_count",
    "prior_avg_amount",
    "prior_std_amount",
    "amount_to_prior_avg_ratio",
    "amount_zscore_vs_prior",
    "insufficient_amount_history",
    "is_new_merchant",
    "is_new_category",
]


def prepare_model_inputs(
    features: pd.DataFrame,
) -> pd.DataFrame:
    inputs = features[FEATURE_COLUMNS].copy()

    boolean_columns = [
        "insufficient_amount_history",
        "is_new_merchant",
        "is_new_category",
    ]

    inputs[boolean_columns] = (
        inputs[boolean_columns].astype(int)
    )

    inputs = inputs.fillna(0.0)

    return inputs


def train_class_weighted_logistic_regression(
    train_features: pd.DataFrame,
) -> Pipeline:
    X_train = prepare_model_inputs(train_features)
    y_train = train_features["is_fraud"]

    model = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(
                    class_weight="balanced",
                    max_iter=1000,
                ),
            ),
        ]
    )

    model.fit(X_train, y_train)

    return model


def predict_fraud_probabilities(
    model: Pipeline,
    features: pd.DataFrame,
) -> pd.Series:
    X = prepare_model_inputs(features)

    probabilities = model.predict_proba(X)[:, 1]

    return pd.Series(
        probabilities,
        index=features.index,
        name="fraud_probability",
    )