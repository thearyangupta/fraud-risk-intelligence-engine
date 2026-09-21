import pandas as pd
from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.models.logistic_regression import (
    FEATURE_COLUMNS,
    predict_fraud_probabilities,
)


def evaluate_logistic_regression(
    model,
    validation_features: pd.DataFrame,
    threshold: float = 0.5,
) -> dict[str, float]:
    y_true = validation_features["is_fraud"]

    probabilities = predict_fraud_probabilities(
        model,
        validation_features,
    )

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


def get_logistic_regression_coefficients(
    model,
) -> pd.DataFrame:
    classifier = model.named_steps["classifier"]

    coefficients = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "coefficient": classifier.coef_[0],
        }
    )

    coefficients["abs_coefficient"] = (
        coefficients["coefficient"].abs()
    )

    return coefficients.sort_values(
        "abs_coefficient",
        ascending=False,
    ).reset_index(drop=True)