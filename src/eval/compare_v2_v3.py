import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.models.logistic_regression import (
    predict_fraud_probabilities,
)
from src.models.tree_models import (
    predict_tree_probabilities,
)


def compute_model_metrics(
    y_true: pd.Series,
    probabilities: pd.Series,
    threshold: float = 0.5,
) -> dict[str, float]:
    predictions = (
        probabilities >= threshold
    ).astype(int)

    return {
        "precision": precision_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "f1": f1_score(
            y_true,
            predictions,
            zero_division=0,
        ),
        "roc_auc": roc_auc_score(
            y_true,
            probabilities,
        ),
        "pr_auc": average_precision_score(
            y_true,
            probabilities,
        ),
    }


def compare_models(
    logistic_model,
    random_forest_model,
    gradient_boosting_model,
    validation_features: pd.DataFrame,
) -> pd.DataFrame:
    y_true = validation_features["is_fraud"]

    logistic_probabilities = (
        predict_fraud_probabilities(
            logistic_model,
            validation_features,
        )
    )

    random_forest_probabilities = (
        predict_tree_probabilities(
            random_forest_model,
            validation_features,
        )
    )

    gradient_boosting_probabilities = (
        predict_tree_probabilities(
            gradient_boosting_model,
            validation_features,
        )
    )

    results = {
        "logistic_regression": compute_model_metrics(
            y_true,
            logistic_probabilities,
        ),
        "random_forest": compute_model_metrics(
            y_true,
            random_forest_probabilities,
        ),
        "gradient_boosting": compute_model_metrics(
            y_true,
            gradient_boosting_probabilities,
        ),
    }

    return pd.DataFrame(results).T