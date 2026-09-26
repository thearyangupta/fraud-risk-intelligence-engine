import pandas as pd
from sklearn.ensemble import IsolationForest

from src.models.logistic_regression import FEATURE_COLUMNS


def prepare_isolation_forest_inputs(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Prepare Week 4 behavioral features for Isolation Forest."""
    return (
        df[FEATURE_COLUMNS]
        .replace([float("inf"), float("-inf")], pd.NA)
        .fillna(0.0)
        .astype(float)
    )


def train_isolation_forest(
    train_df: pd.DataFrame,
    contamination: float = 0.01,
    random_state: int = 42,
) -> IsolationForest:
    """Train Isolation Forest using features only."""
    X_train = prepare_isolation_forest_inputs(train_df)

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=random_state,
        n_jobs=-1,
    )

    model.fit(X_train)

    return model


def get_anomaly_scores(
    model: IsolationForest,
    df: pd.DataFrame,
) -> pd.Series:
    """Return scores where larger values mean more anomalous."""
    X = prepare_isolation_forest_inputs(df)

    scores = -model.score_samples(X)

    return pd.Series(
        scores,
        index=df.index,
        name="anomaly_score",
    )


def predict_anomalies(
    model: IsolationForest,
    df: pd.DataFrame,
) -> pd.Series:
    """Return 1 for anomaly and 0 for normal transaction."""
    X = prepare_isolation_forest_inputs(df)

    predictions = model.predict(X)

    return pd.Series(
        (predictions == -1).astype(int),
        index=df.index,
        name="anomaly_prediction",
    )