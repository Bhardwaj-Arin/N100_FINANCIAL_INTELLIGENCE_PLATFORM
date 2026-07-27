"""
Company Feature Engineering
"""

from __future__ import annotations

import numpy as np

from src.feature_engineering.base import BaseFeatureEngineer


class CompanyFeatureEngineer(BaseFeatureEngineer):

    def __init__(self, df):

        super().__init__(df)

        self.df = self.df.rename(
            columns={
                "id": "company_id"
            }
        )

        self.validate_columns([
            "company_id",
            "company_name",
            "website",
            "book_value",
            "roce_percentage",
            "roe_percentage"
        ])

    # -------------------------------------------------

    def engineer_name_length(self):

        self.df["company_name_length"] = (
            self.df["company_name"]
            .str.len()
        )

    # -------------------------------------------------

    def engineer_name_word_count(self):

        self.df["company_name_word_count"] = (
            self.df["company_name"]
            .str.split()
            .str.len()
        )

    # -------------------------------------------------

    def engineer_has_website(self):

        self.df["has_website"] = np.where(
            self.df["website"].notna(),
            1,
            0
        )

    # -------------------------------------------------

    def engineer_high_roe(self):

        self.df["high_roe"] = np.where(
            self.df["roe_percentage"] >= 20,
            1,
            0
        )

    # -------------------------------------------------

    def engineer_high_roce(self):

        self.df["high_roce"] = np.where(
            self.df["roce_percentage"] >= 20,
            1,
            0
        )

    # -------------------------------------------------

    def engineer_book_value_positive(self):

        self.df["positive_book_value"] = np.where(
            self.df["book_value"] > 0,
            1,
            0
        )

    # -------------------------------------------------

    def run(self):

        self.engineer_name_length()

        self.engineer_name_word_count()

        self.engineer_has_website()

        self.engineer_high_roe()

        self.engineer_high_roce()

        self.engineer_book_value_positive()

        return self.df