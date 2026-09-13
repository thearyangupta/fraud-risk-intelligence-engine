import numpy as np
import pandas as pd


def add_amount_features(
    df: pd.DataFrame,
    customer_col: str = "cc_num",
    timestamp_col: str = "trans_date_trans_time",
    amount_col: str = "amt",
) -> pd.DataFrame:
    result = df.copy()

    result[timestamp_col] = pd.to_datetime(
        result[timestamp_col]
    )

    result["_original_order"] = np.arange(len(result))

    result = result.sort_values(
        [customer_col, timestamp_col, "_original_order"]
    ).reset_index(drop=True)

    grouped_amount = result.groupby(
        customer_col,
        sort=False,
    )[amount_col]

    result["prior_txn_count"] = result.groupby(
        customer_col,
        sort=False,
    ).cumcount()

    result["prior_avg_amount"] = grouped_amount.transform(
        lambda amounts: (
            amounts
            .expanding(min_periods=1)
            .mean()
            .shift(1)
        )
    )

    result["prior_std_amount"] = grouped_amount.transform(
        lambda amounts: (
            amounts
            .expanding(min_periods=2)
            .std(ddof=1)
            .shift(1)
        )
    )

    result["amount_to_prior_avg_ratio"] = (
        result[amount_col]
        / result["prior_avg_amount"].replace(0, np.nan)
    )

    valid_zscore = (
        result["prior_std_amount"].notna()
        & (result["prior_std_amount"] > 0)
    )

    result["amount_zscore_vs_prior"] = np.nan

    result.loc[
        valid_zscore,
        "amount_zscore_vs_prior",
    ] = (
        (
            result.loc[valid_zscore, amount_col]
            - result.loc[valid_zscore, "prior_avg_amount"]
        )
        / result.loc[valid_zscore, "prior_std_amount"]
    )

    result["insufficient_amount_history"] = (
        result["prior_txn_count"] < 2
    )

    result = (
        result.sort_values("_original_order")
        .drop(columns="_original_order")
        .reset_index(drop=True)
    )

    return result