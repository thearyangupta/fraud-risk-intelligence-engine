import numpy as np
import pandas as pd

VELOCITY_WINDOWS = {
    "txn_count_10m_before": pd.Timedelta(minutes=10),
    "txn_count_1h_before": pd.Timedelta(hours=1),
    "txn_count_24h_before": pd.Timedelta(hours=24),
}


def add_velocity_features(
    df: pd.DataFrame,
    customer_col: str = "cc_num",
    timestamp_col: str = "trans_date_trans_time",
) -> pd.DataFrame:
    result = df.copy()

    result[timestamp_col] = pd.to_datetime(
        result[timestamp_col]
    )

    result["_original_order"] = np.arange(len(result))

    result = result.sort_values(
        [customer_col, timestamp_col, "_original_order"]
    ).reset_index(drop=True)

    result["seconds_since_prev_txn"] = (
        result[timestamp_col]
        - result.groupby(customer_col)[timestamp_col].shift(1)
    ).dt.total_seconds()

    for feature_name, window in VELOCITY_WINDOWS.items():
        counts = np.zeros(len(result), dtype=np.int64)

        for _, group in result.groupby(
            customer_col,
            sort=False,
        ):
            timestamps = group[timestamp_col].to_numpy(
                dtype="datetime64[ns]"
            )

            window_delta = window.to_timedelta64()

            left_boundary = np.searchsorted(
                timestamps,
                timestamps - window_delta,
                side="left",
            )

            current_boundary = np.searchsorted(
                timestamps,
                timestamps,
                side="left",
            )

            counts[group.index] = (
                current_boundary - left_boundary
            )

        result[feature_name] = counts

    result = (
        result.sort_values("_original_order")
        .drop(columns="_original_order")
        .reset_index(drop=True)
    )

    return result