import pandas as pd

from src.features.amount import add_amount_features
from src.features.novelty import add_novelty_features
from src.features.velocity import add_velocity_features


def build_features(
    df: pd.DataFrame,
    split_name: str,
) -> pd.DataFrame:
    features = df.copy()

    features = add_velocity_features(features)

    features = add_amount_features(features)

    features = add_novelty_features(features)

    features["split"] = split_name

    return features