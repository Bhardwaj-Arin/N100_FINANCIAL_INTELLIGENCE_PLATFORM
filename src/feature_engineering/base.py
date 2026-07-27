"""
Base class for all feature engineering modules.
"""

from __future__ import annotations

import pandas as pd


class BaseFeatureEngineer:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def validate_columns(self, required_columns):

        missing = [
            column
            for column in required_columns
            if column not in self.df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns: {missing}"
            )

    def get_dataframe(self):
        return self.df