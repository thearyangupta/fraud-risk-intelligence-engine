import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_integer_dtype,
    is_numeric_dtype,
)


def validate_schema(df: pd.DataFrame) -> None:
    required_columns = {
        "trans_date_trans_time",
        "amt",
        "is_fraud",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    if not is_datetime64_any_dtype(df["trans_date_trans_time"]):
        raise TypeError(
            "trans_date_trans_time must be datetime-like"
        )

    if not is_numeric_dtype(df["amt"]):
        raise TypeError(
            "amt must be numeric"
        )

    if not is_integer_dtype(df["is_fraud"]):
        raise TypeError(
            "is_fraud must be integer-like"
        )


def validate_ranges(
    df: pd.DataFrame,
    min_timestamp: pd.Timestamp,
    max_timestamp: pd.Timestamp,
) -> None:
    if (df["amt"] < 0).any():
        raise ValueError("amt contains negative values")

    if (df["trans_date_trans_time"] < min_timestamp).any():
        raise ValueError(
            "trans_date_trans_time contains values before the allowed minimum"
        )

    if (df["trans_date_trans_time"] > max_timestamp).any():
        raise ValueError(
            "trans_date_trans_time contains values after the allowed maximum"
        )

    invalid_labels = ~df["is_fraud"].isin([0, 1])

    if invalid_labels.any():
        raise ValueError("is_fraud must contain only 0 or 1")


def validate_nulls(
    df: pd.DataFrame,
    required_columns: list[str],
) -> None:
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Cannot check nulls because columns are missing: {missing_columns}"
        )

    null_counts = df[required_columns].isna().sum()

    columns_with_nulls = null_counts[null_counts > 0]

    if not columns_with_nulls.empty:
        raise ValueError(
            f"Required columns contain nulls: "
            f"{columns_with_nulls.to_dict()}"
        )

def validate_label_sanity(
    df: pd.DataFrame,
    min_fraud_rate: float,
    max_fraud_rate: float,
) -> None:
    fraud_rate = df["is_fraud"].mean()

    if fraud_rate < min_fraud_rate or fraud_rate > max_fraud_rate:
        raise ValueError(
            f"Fraud rate {fraud_rate:.4f} is outside the "
            f"expected range [{min_fraud_rate:.4f}, {max_fraud_rate:.4f}]"
        )