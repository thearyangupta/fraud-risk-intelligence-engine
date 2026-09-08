import os
from io import StringIO

import pandas as pd
import psycopg

from src.data.split import temporal_split

RAW_DATA_PATH = "data/fraudTrain.csv"

CUSTOMER_COLUMNS = [
    "cc_num",
    "first",
    "last",
    "gender",
    "street",
    "city",
    "state",
    "zip",
    "lat",
    "long",
    "city_pop",
    "job",
    "dob",
]

TRANSACTION_COLUMNS = [
    "trans_num",
    "cc_num",
    "amt",
    "merchant",
    "category",
    "trans_date_trans_time",
    "merch_lat",
    "merch_long",
    "is_fraud",
]


def get_connection():
    return psycopg.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        dbname=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )


def build_customers(df: pd.DataFrame) -> pd.DataFrame:
    customers = df[CUSTOMER_COLUMNS].copy()

    customers["dob"] = pd.to_datetime(customers["dob"]).dt.date

    static_columns = [
        column
        for column in CUSTOMER_COLUMNS
        if column != "cc_num"
    ]

    consistency = (
        customers.groupby("cc_num")[static_columns]
        .nunique(dropna=False)
    )

    inconsistent = consistency.gt(1).any(axis=1)

    if inconsistent.any():
        raise ValueError(
            "Some customer IDs have inconsistent static attributes"
        )

    customers = customers.drop_duplicates(
        subset=["cc_num"]
    ).reset_index(drop=True)

    return customers


def prepare_transactions(
    df: pd.DataFrame,
    split_name: str,
) -> pd.DataFrame:
    transactions = df[TRANSACTION_COLUMNS].copy()

    transactions["trans_date_trans_time"] = pd.to_datetime(
        transactions["trans_date_trans_time"]
    )

    transactions["split"] = split_name

    return transactions


def copy_dataframe(
    connection,
    table_name: str,
    columns: list[str],
    df: pd.DataFrame,
    chunk_size: int = 100_000,
) -> None:
    column_sql = ", ".join(columns)

    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start:start + chunk_size]

        buffer = StringIO()

        chunk.to_csv(
            buffer,
            index=False,
            header=False,
            na_rep="",
        )

        buffer.seek(0)

        with connection.cursor() as cursor, cursor.copy(
                f"""
                COPY {table_name} ({column_sql})
                FROM STDIN
                WITH (FORMAT CSV)
                """
            ) as copy:
                copy.write(buffer.getvalue())


def main():
    print("Loading raw transaction data...")

    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Raw rows: {len(df):,}")

    print("Recreating Week 2 temporal split...")

    train, val, test = temporal_split(df)

    print(
        f"train={len(train):,}, "
        f"val={len(val):,}, "
        f"test={len(test):,}"
    )

    print("Building customer table...")

    customers = build_customers(df)

    customer_db = customers.rename(
        columns={
            "cc_num": "customer_id",
            "first": "first_name",
            "last": "last_name",
            "zip": "zip",
            "lat": "latitude",
            "long": "longitude",
            "city_pop": "city_population",
            "dob": "date_of_birth",
        }
    )

    print(f"Unique customers: {len(customer_db):,}")

    train_db = prepare_transactions(train, "train")
    val_db = prepare_transactions(val, "val")
    test_db = prepare_transactions(test, "test")

    rename_map = {
        "trans_num": "transaction_id",
        "cc_num": "customer_id",
        "amt": "amount",
        "trans_date_trans_time": "timestamp",
        "merch_lat": "merchant_latitude",
        "merch_long": "merchant_longitude",
        "is_fraud": "fraud_label",
    }

    train_db = train_db.rename(columns=rename_map)
    val_db = val_db.rename(columns=rename_map)
    test_db = test_db.rename(columns=rename_map)

    customer_db_columns = [
        "customer_id",
        "first_name",
        "last_name",
        "gender",
        "street",
        "city",
        "state",
        "zip",
        "latitude",
        "longitude",
        "city_population",
        "job",
        "date_of_birth",
    ]

    transaction_db_columns = [
        "transaction_id",
        "customer_id",
        "amount",
        "merchant",
        "category",
        "timestamp",
        "merchant_latitude",
        "merchant_longitude",
        "fraud_label",
        "split",
    ]

    print("Connecting to PostgreSQL...")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE transactions")
            cursor.execute(
                "TRUNCATE TABLE customers CASCADE"
            )

        print("Loading customers...")

        copy_dataframe(
            connection,
            "customers",
            customer_db_columns,
            customer_db[customer_db_columns],
        )

        print("Loading train transactions...")

        copy_dataframe(
            connection,
            "transactions",
            transaction_db_columns,
            train_db[transaction_db_columns],
        )

        print("Loading validation transactions...")

        copy_dataframe(
            connection,
            "transactions",
            transaction_db_columns,
            val_db[transaction_db_columns],
        )

        print("Loading test transactions...")

        copy_dataframe(
            connection,
            "transactions",
            transaction_db_columns,
            test_db[transaction_db_columns],
        )

    print("PostgreSQL load complete.")


if __name__ == "__main__":
    main()