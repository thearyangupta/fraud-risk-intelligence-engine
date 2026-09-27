import pandas as pd
from sklearn.metrics import precision_score, recall_score


def evaluate_thresholds(
    y_true: pd.Series,
    probabilities: pd.Series,
    thresholds: list[float],
) -> pd.DataFrame:
    """Evaluate binary decision thresholds against validation labels."""

    rows = []

    for threshold in thresholds:
        predictions = (
            probabilities >= threshold
        ).astype(int)

        precision = precision_score(
            y_true,
            predictions,
            zero_division=0,
        )

        recall = recall_score(
            y_true,
            predictions,
            zero_division=0,
        )

        flagged = int(predictions.sum())

        rows.append(
            {
                "threshold": threshold,
                "precision": precision,
                "recall": recall,
                "flagged": flagged,
                "flag_rate": flagged / len(y_true),
            }
        )

    return pd.DataFrame(rows)