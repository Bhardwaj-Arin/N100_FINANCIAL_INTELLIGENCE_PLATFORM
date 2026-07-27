"""
Market Feature Engineering
"""

from __future__ import annotations

import numpy as np

from src.feature_engineering.base import BaseFeatureEngineer


class MarketFeatureEngineer(BaseFeatureEngineer):

    def __init__(self, df):

        super().__init__(df)

        self.validate_columns([
            "market_cap_crore",
            "enterprise_value_crore",
            "pe_ratio",
            "pb_ratio",
            "ev_ebitda",
            "dividend_yield_pct"
        ])

    # -------------------------------------------------

    def engineer_market_cap(self):

        cap = self.df["market_cap_crore"]

        self.df["market_cap_category"] = np.select(
            [
                cap >= 200000,
                cap >= 50000,
                cap >= 10000,
                cap < 10000
            ],
            [
                "Mega Cap",
                "Large Cap",
                "Mid Cap",
                "Small Cap"
            ],
            default="Unknown"
        )

    # -------------------------------------------------

    def engineer_pe(self):

        pe = self.df["pe_ratio"]

        self.df["pe_category"] = np.select(
            [
                pe <= 15,
                pe <= 30,
                pe > 30
            ],
            [
                "Undervalued",
                "Fairly Valued",
                "Overvalued"
            ],
            default="Unknown"
        )

    # -------------------------------------------------

    def engineer_pb(self):

        pb = self.df["pb_ratio"]

        self.df["pb_category"] = np.select(
            [
                pb <= 1,
                pb <= 3,
                pb > 3
            ],
            [
                "Undervalued",
                "Fairly Valued",
                "Premium"
            ],
            default="Unknown"
        )

    # -------------------------------------------------

    def engineer_dividend(self):

        dividend = self.df["dividend_yield_pct"]

        self.df["dividend_paying_company"] = (
            dividend > 0
        ).astype(int)

    # -------------------------------------------------

    def engineer_value_score(self):

        pe_score = np.select(
            [
                self.df["pe_ratio"] <= 15,
                self.df["pe_ratio"] <= 30,
                self.df["pe_ratio"] > 30
            ],
            [
                3,
                2,
                1
            ],
            default=0
        )

        pb_score = np.select(
            [
                self.df["pb_ratio"] <= 1,
                self.df["pb_ratio"] <= 3,
                self.df["pb_ratio"] > 3
            ],
            [
                3,
                2,
                1
            ],
            default=0
        )

        self.df["value_score"] = pe_score + pb_score

    # -------------------------------------------------

    def run(self):

        self.engineer_market_cap()

        self.engineer_pe()

        self.engineer_pb()

        self.engineer_dividend()

        self.engineer_value_score()

        return self.df