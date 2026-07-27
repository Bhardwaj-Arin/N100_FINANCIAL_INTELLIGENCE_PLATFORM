"""
cleaner.py
----------------------------------------
Generic Data Cleaning Module
"""

import pandas as pd


class DataCleaner:
    """
    Generic cleaner for all structured datasets.
    """

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]

        # Standardize column names
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )

        # Strip whitespace from string columns
        object_cols = df.select_dtypes(include=["object"]).columns

        for col in object_cols:
            df[col] = df[col].astype(str).str.strip()

        return df