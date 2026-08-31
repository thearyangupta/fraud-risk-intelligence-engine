import pandas as pd
import pytest

from src.data.validation import (
    validate_label_sanity,
    validate_nulls,
    validate_ranges,
    validate_schema,
)


def make_valid_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "trans_date_trans_time": pd.to_datetime(
                [
                    "2019-01-01 10:00:00",
                    "2019-01-02 11:00:00",
                ]
            ),
            "amt": [100.0, 250.0],
            "is_fraud": [0, 1],
        }
    )

# Schema validation tests

def test_validate_schema_passes_for_valid_data():
    df = make_valid_dataframe()

    validate_schema(df)


def test_validate_schema_raises_for_missing_column():
    df = make_valid_dataframe()

    df = df.drop(columns=["amt"])

    with pytest.raises(ValueError):
        validate_schema(df)

# Range validation tests


def test_validate_ranges_passes_for_valid_data():
    df = make_valid_dataframe()

    validate_ranges(
        df,
        min_timestamp=pd.Timestamp("2019-01-01"),
        max_timestamp=pd.Timestamp("2019-12-31"),
    )


def test_validate_ranges_raises_for_negative_amount():
    df = make_valid_dataframe()

    df.loc[0, "amt"] = -50.0

    with pytest.raises(ValueError):
        validate_ranges(
            df,
            min_timestamp=pd.Timestamp("2019-01-01"),
            max_timestamp=pd.Timestamp("2019-12-31"),
        )


def test_validate_ranges_raises_for_invalid_label():
    df = make_valid_dataframe()

    df.loc[0, "is_fraud"] = 7

    with pytest.raises(ValueError):
        validate_ranges(
            df,
            min_timestamp=pd.Timestamp("2019-01-01"),
            max_timestamp=pd.Timestamp("2019-12-31"),
        )


def test_validate_ranges_raises_for_timestamp_outside_window():
    df = make_valid_dataframe()

    df.loc[0, "trans_date_trans_time"] = pd.Timestamp(
        "2020-01-01 10:00:00"
    )

    with pytest.raises(ValueError):
        validate_ranges(
            df,
            min_timestamp=pd.Timestamp("2019-01-01"),
            max_timestamp=pd.Timestamp("2019-12-31"),
        )


# Null validation tests

def test_validate_nulls_passes_for_valid_data():
    df = make_valid_dataframe()

    validate_nulls(
        df,
        required_columns=[
            "trans_date_trans_time",
            "amt",
            "is_fraud",
        ],
    )


def test_validate_nulls_raises_when_required_column_has_null():
    df = make_valid_dataframe()

    df.loc[0, "amt"] = None

    with pytest.raises(ValueError):
        validate_nulls(
            df,
            required_columns=[
                "trans_date_trans_time",
                "amt",
                "is_fraud",
            ],
        )


def test_validate_nulls_raises_when_required_column_is_missing():
    df = make_valid_dataframe()

    df = df.drop(columns=["amt"])

    with pytest.raises(ValueError):
        validate_nulls(
            df,
            required_columns=[
                "trans_date_trans_time",
                "amt",
                "is_fraud",
            ],
        )

# Label-sanity validation tests

def test_validate_label_sanity_passes_for_plausible_rate():
    df = make_valid_dataframe()

    validate_label_sanity(
        df,
        min_fraud_rate=0.0,
        max_fraud_rate=1.0,
    )


def test_validate_label_sanity_raises_for_implausible_rate():
    df = pd.DataFrame(
        {
            "trans_date_trans_time": pd.to_datetime(
                [
                    "2019-01-01 10:00:00",
                    "2019-01-02 11:00:00",
                    "2019-01-03 12:00:00",
                    "2019-01-04 13:00:00",
                ]
            ),
            "amt": [
                100.0,
                200.0,
                300.0,
                400.0,
            ],
            "is_fraud": [
                1,
                1,
                1,
                1,
            ],
        }
    )

    with pytest.raises(ValueError):
        validate_label_sanity(
            df,
            min_fraud_rate=0.001,
            max_fraud_rate=0.02,
        )