import pandas as pd


class DataPreprocessor:

    def preprocess(self, df: pd.DataFrame):

        df = df.copy()

        # ------------------------
        # Remove duplicate rows
        # ------------------------

        df.drop_duplicates(inplace=True)

        # ------------------------
        # Remove duplicate columns
        # ------------------------

        df = df.loc[:, ~df.columns.duplicated()]

        # ------------------------
        # Standardize column names
        # ------------------------

        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )

        # ------------------------
        # Strip string columns
        # ------------------------

        object_columns = df.select_dtypes(include="object").columns

        for col in object_columns:

            df[col] = df[col].astype(str).str.strip()

        # ------------------------
        # Fill numeric missing values
        # ------------------------

        numeric = df.select_dtypes(include="number").columns

        for col in numeric:

            df[col] = df[col].fillna(df[col].median())

        # ------------------------
        # Fill categorical values
        # ------------------------

        categorical = df.select_dtypes(include="object").columns

        for col in categorical:

            df[col] = df[col].fillna("Unknown")

        return df