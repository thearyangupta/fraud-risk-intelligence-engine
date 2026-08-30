import pandas as pd


class CategoricalPreprocessor:
    def __init__(self, categorical_columns: list[str]):
        self.categorical_columns = categorical_columns
        self.category_maps: dict[str, dict[object, int]] = {}

    def fit(self, train_df: pd.DataFrame):
        for column in self.categorical_columns:
            categories = sorted(train_df[column].dropna().unique())

            self.category_maps[column] = {
                category: index
                for index, category in enumerate(categories)
            }

        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        transformed = df.copy()

        for column in self.categorical_columns:
            mapping = self.category_maps[column]

            transformed[column] = (
                transformed[column]
                .map(mapping)
                .fillna(-1)
                .astype(int)
            )

        return transformed