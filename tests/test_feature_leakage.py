import pandas as pd
import pytest

from src.features.build import build_features


def test_prior_average_uses_only_past_transactions():
    df = pd.DataFrame(
        {
            "cc_num": [1, 1, 1, 1],
            "trans_date_trans_time": [
                "2026-01-01 10:00:00",
                "2026-01-01 11:00:00",
                "2026-01-01 12:00:00",
                "2026-01-01 13:00:00",
            ],
            "amt": [
                100.0,
                200.0,
                900.0,
                400.0,
            ],
            "merchant": [
                "A",
                "B",
                "C",
                "D",
            ],
            "category": [
                "food",
                "travel",
                "shopping",
                "fuel",
            ],
        }
    )

    features = build_features(
        df,
        split_name="train",
    )

    expected_prior_average = (
        100.0 + 200.0
    ) / 2

    actual_prior_average = features.loc[
        2,
        "prior_avg_amount",
    ]

    assert actual_prior_average == pytest.approx(
        expected_prior_average
    )