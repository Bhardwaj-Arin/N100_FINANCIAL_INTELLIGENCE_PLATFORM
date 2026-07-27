"""
Sector Feature Engineering
"""

from __future__ import annotations

import numpy as np

from src.feature_engineering.base import BaseFeatureEngineer


class SectorFeatureEngineer(BaseFeatureEngineer):

    def __init__(self, df):

        super().__init__(df)

        self.validate_columns([
            "broad_sector",
            "sub_sector",
            "market_cap_category",
            "index_weight_pct"
        ])

    # -------------------------------------------------

    def engineer_sector_code(self):

        self.df["sector_code"] = (
            self.df["broad_sector"]
            .astype("category")
            .cat.codes
        )

    # -------------------------------------------------

    def engineer_subsector_code(self):

        self.df["subsector_code"] = (
            self.df["sub_sector"]
            .astype("category")
            .cat.codes
        )

    # -------------------------------------------------

    def engineer_sector_company_count(self):

        self.df["sector_company_count"] = (
            self.df.groupby("broad_sector")["company_id"]
            .transform("count")
        )

    # -------------------------------------------------

    def engineer_subsector_company_count(self):

        self.df["subsector_company_count"] = (
            self.df.groupby("sub_sector")["company_id"]
            .transform("count")
        )

    # -------------------------------------------------

    def engineer_sector_rank(self):

        sector_rank = (
            self.df.groupby("broad_sector")["company_id"]
            .count()
            .rank(method="dense", ascending=False)
        )

        self.df["sector_rank"] = (
            self.df["broad_sector"]
            .map(sector_rank)
        )

    # -------------------------------------------------

    def engineer_large_sector(self):

        self.df["large_sector"] = np.where(
            self.df["sector_company_count"] >= 10,
            1,
            0
        )

    # -------------------------------------------------

    def run(self):

        self.engineer_sector_code()

        self.engineer_subsector_code()

        self.engineer_sector_company_count()

        self.engineer_subsector_company_count()

        self.engineer_sector_rank()

        self.engineer_large_sector()

        return self.df