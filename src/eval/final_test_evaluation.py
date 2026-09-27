import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.decision.engine import make_decision
from src.features.build import build_features
from src.models.tree_models import (
    predict_tree_probabilities,
    train_gradient_boosting,
)


def evaluate_locked_policy(
    train: pd.DataFrame,
    test: pd.DataFrame,
) -> tuple[dict[str, float], pd.DataFrame]:
    """Evaluate the frozen v3 model and decision policy on held-out test data."""

    train_features = build_features(
        train,
        split_name="train",
    )

    test_features = build_features(
        test,
        split_name="test",
    )

    model = train_gradient_boosting(
        train_features
    )

    probabilities = predict_tree_probabilities(
        model,
        test_features,
    )

    y_true = test_features["is_fraud"]

    binary_predictions = (
        probabilities >= 0.50
    ).astype(int)

    metrics = {
        "precision": precision_score(
            y_true,
            binary_predictions,
            zero_division=0,
        ),
        "recall": recall_score(
            y_true,
            binary_predictions,
            zero_division=0,
        ),
        "f1": f1_score(
            y_true,
            binary_predictions,
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

    results = test_features[
        ["is_fraud"]
    ].copy()

    results["fraud_probability"] = probabilities

    results["decision"] = [
        make_decision(float(score))
        for score in probabilities
    ]

    return metrics, results