import pandas as pd


def apply_rule_baseline(
    features: pd.DataFrame,
    amount_ratio_threshold: float = 5.0,
    velocity_1h_threshold: int = 3,
) -> pd.DataFrame:
    result = features.copy()

    amount_and_novelty_rule = (
        (result["amount_to_prior_avg_ratio"] > amount_ratio_threshold)
        & result["is_new_merchant"]
    )

    velocity_rule = (
        result["txn_count_1h_before"] > velocity_1h_threshold
    )

    result["rule_prediction"] = (
        amount_and_novelty_rule | velocity_rule
    ).astype(int)

    result["rule_reason"] = "none"

    result.loc[
        amount_and_novelty_rule,
        "rule_reason",
    ] = "high_amount_and_new_merchant"

    result.loc[
        velocity_rule,
        "rule_reason",
    ] = "high_velocity"

    result.loc[
        amount_and_novelty_rule & velocity_rule,
        "rule_reason",
    ] = "high_amount_and_new_merchant+high_velocity"

    return result