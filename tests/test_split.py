import pandas as pd

from src.data.split import temporal_split


def test_temporal_split_preserves_time_order():
    df = pd.DataFrame(
        {
            "trans_date_trans_time": pd.to_datetime(
                [
                    "2019-01-05 10:00:00",
                    "2019-01-01 10:00:00",
                    "2019-01-04 10:00:00",
                    "2019-01-02 10:00:00",
                    "2019-01-06 10:00:00",
                    "2019-01-03 10:00:00",
                    "2019-01-07 10:00:00",
                    "2019-01-08 10:00:00",
                    "2019-01-09 10:00:00",
                    "2019-01-10 10:00:00",
                ]
            ),
            "amt": [
                50.0,
                100.0,
                75.0,
                200.0,
                25.0,
                300.0,
                150.0,
                80.0,
                90.0,
                120.0,
            ],
            "is_fraud": [
                0,
                0,
                1,
                0,
                0,
                1,
                0,
                0,
                0,
                1,
            ],
        }
    )

    train, val, test = temporal_split(df)

    assert (
        train["trans_date_trans_time"].max()
        <= val["trans_date_trans_time"].min()
    )

    assert (
        val["trans_date_trans_time"].max()
        <= test["trans_date_trans_time"].min()
    )

    assert (
        train["trans_date_trans_time"].max()
        <= test["trans_date_trans_time"].min()
    )