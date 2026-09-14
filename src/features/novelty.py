import numpy as np
import pandas as pd


def add_novelty_features(
    df: pd.DataFrame,
    customer_col: str = "cc_num",
    timestamp_col: str = "trans_date_trans_time",
    merchant_col: str = "merchant",
    category_col: str = "category",
) -> pd.DataFrame:
    result = df.copy()

    result[timestamp_col] = pd.to_datetime(
        result[timestamp_col]
    )

    result["_original_order"] = np.arange(len(result))

    result = result.sort_values(
        [customer_col, timestamp_col, "_original_order"]
    ).reset_index(drop=True)

    result["is_new_merchant"] = False
    result["is_new_category"] = False

    for _, group in result.groupby(
        customer_col,
        sort=False,
    ):
        seen_merchants = set()
        seen_categories = set()

        for index in group.index:
            merchant = result.at[index, merchant_col]
            category = result.at[index, category_col]

            result.at[index, "is_new_merchant"] = (
                merchant not in seen_merchants
            )

            result.at[index, "is_new_category"] = (
                category not in seen_categories
            )

            seen_merchants.add(merchant)
            seen_categories.add(category)

    result = (
        result.sort_values("_original_order")
        .drop(columns="_original_order")
        .reset_index(drop=True)
    )

    return result