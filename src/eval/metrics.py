import pandas as pd


def compute_binary_metrics(
    df: pd.DataFrame,
    label_col: str = "is_fraud",
    prediction_col: str = "rule_prediction",
) -> dict[str, float | int]:
    actual = df[label_col]
    predicted = df[prediction_col]

    true_positive = int(
        ((actual == 1) & (predicted == 1)).sum()
    )

    false_positive = int(
        ((actual == 0) & (predicted == 1)).sum()
    )

    true_negative = int(
        ((actual == 0) & (predicted == 0)).sum()
    )

    false_negative = int(
        ((actual == 1) & (predicted == 0)).sum()
    )

    total = len(df)

    accuracy = (
        (true_positive + true_negative) / total
        if total
        else 0.0
    )

    precision_denominator = (
        true_positive + false_positive
    )

    precision = (
        true_positive / precision_denominator
        if precision_denominator
        else 0.0
    )

    recall_denominator = (
        true_positive + false_negative
    )

    recall = (
        true_positive / recall_denominator
        if recall_denominator
        else 0.0
    )

    f1_denominator = precision + recall

    f1 = (
        2 * precision * recall / f1_denominator
        if f1_denominator
        else 0.0
    )

    return {
        "true_positive": true_positive,
        "false_positive": false_positive,
        "true_negative": true_negative,
        "false_negative": false_negative,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }