"""
Financial Ratio Feature Engineering
"""

from __future__ import annotations

import numpy as np

from src.feature_engineering.base import BaseFeatureEngineer


class FinancialRatioEngineer(BaseFeatureEngineer):

    def __init__(self, df):

        super().__init__(df)

        self.validate_columns([
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr",
            "capex_cr",
            "earnings_per_share",
            "book_value_per_share",
            "dividend_payout_ratio_pct",
            "total_debt_cr",
            "cash_from_operations_cr"
        ])

    # -------------------------------------------------
    # Profitability Features
    # -------------------------------------------------

    def engineer_profitability(self):

        profit = self.df["net_profit_margin_pct"]

        self.df["profit_margin_category"] = np.select(
            [
                profit >= 20,
                profit >= 10,
                profit >= 0,
                profit < 0
            ],
            [
                "Excellent",
                "Good",
                "Average",
                "Loss Making"
            ],
            default="Unknown"
        )

        self.df["high_profitability"] = (
            profit >= 20
        ).astype(int)

        self.df["profitability_score"] = np.select(
            [
                profit >= 20,
                profit >= 10,
                profit >= 0,
                profit < 0
            ],
            [
                4,
                3,
                2,
                1
            ],
            default=0
        )

    # -------------------------------------------------
    # ROE Features
    # -------------------------------------------------

    def engineer_roe(self):

        roe = self.df["return_on_equity_pct"]

        self.df["roe_grade"] = np.select(
            [
                roe >= 25,
                roe >= 15,
                roe >= 5,
                roe < 5
            ],
            [
                "A",
                "B",
                "C",
                "D"
            ],
            default="NA"
        )

        self.df["high_roe"] = (
            roe >= 20
        ).astype(int)

        self.df["roe_score"] = np.select(
            [
                roe >= 25,
                roe >= 15,
                roe >= 5,
                roe < 5
            ],
            [
                4,
                3,
                2,
                1
            ],
            default=0
        )

    # -------------------------------------------------
    # Debt Features
    # -------------------------------------------------

    def engineer_debt(self):

        debt = self.df["debt_to_equity"]

        self.df["debt_risk"] = np.select(
            [
                debt <= 0.5,
                debt <= 1.0,
                debt <= 2.0,
                debt > 2.0
            ],
            [
                "Low",
                "Moderate",
                "High",
                "Very High"
            ],
            default="Unknown"
        )

        self.df["safe_debt"] = (
            debt <= 1
        ).astype(int)

        self.df["debt_score"] = np.select(
            [
                debt <= 0.5,
                debt <= 1.0,
                debt <= 2.0,
                debt > 2.0
            ],
            [
                4,
                3,
                2,
                1
            ],
            default=0
        )

    # -------------------------------------------------
    # Cash Flow Features
    # -------------------------------------------------

    def engineer_cashflow(self):

        cash = self.df["free_cash_flow_cr"]

        self.df["positive_cashflow"] = (
            cash > 0
        ).astype(int)

        self.df["cashflow_category"] = np.select(
            [
                cash >= 1000,
                cash >= 100,
                cash > 0,
                cash <= 0
            ],
            [
                "Strong",
                "Healthy",
                "Positive",
                "Negative"
            ],
            default="Unknown"
        )

    # -------------------------------------------------
    # Dividend Features
    # -------------------------------------------------

    def engineer_dividend(self):

        dividend = self.df["dividend_payout_ratio_pct"]

        self.df["dividend_company"] = (
            dividend > 0
        ).astype(int)

        self.df["dividend_category"] = np.select(
            [
                dividend >= 60,
                dividend >= 30,
                dividend > 0,
                dividend == 0
            ],
            [
                "High",
                "Medium",
                "Low",
                "No Dividend"
            ],
            default="Unknown"
        )

    # -------------------------------------------------
    # Efficiency Features
    # -------------------------------------------------

    def engineer_efficiency(self):

        asset = self.df["asset_turnover"]

        self.df["asset_efficiency"] = np.select(
            [
                asset >= 2,
                asset >= 1,
                asset >= 0.5,
                asset < 0.5
            ],
            [
                "Excellent",
                "Good",
                "Average",
                "Poor"
            ],
            default="Unknown"
        )

    # -------------------------------------------------
    # Composite Score
    # -------------------------------------------------

    def engineer_financial_strength(self):

        self.df["financial_strength_score"] = (
            self.df["profitability_score"] +
            self.df["roe_score"] +
            self.df["debt_score"]
        )

    # -------------------------------------------------

    def run(self):

        self.engineer_profitability()

        self.engineer_roe()

        self.engineer_debt()

        self.engineer_cashflow()

        self.engineer_dividend()

        self.engineer_efficiency()

        self.engineer_financial_strength()

        return self.df