import pandas as pd


def temporal_split(
    df: pd.DataFrame,
    timestamp_col: str = "trans_date_trans_time",
    train_ratio: float = 0.70,
    val_ratio: float = 0.15,
):
    df = df.copy()

    df[timestamp_col] = pd.to_datetime(df[timestamp_col])

    df = df.sort_values(timestamp_col).reset_index(drop=True)

    n = len(df)

    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    train = df.iloc[:train_end].copy()
    val = df.iloc[train_end:val_end].copy()
    test = df.iloc[val_end:].copy()

    return train, val, test