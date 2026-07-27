"""
Price Feature Engineering
"""

from __future__ import annotations

from src.feature_engineering.base import BaseFeatureEngineer


class PriceFeatureEngineer(BaseFeatureEngineer):

    def __init__(self, df):

        super().__init__(df)

        self.validate_columns([
            "company_id",
            "date",
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "adjusted_close",
            "volume"
        ])

        self.df["date"] = self.df["date"].astype("datetime64[ns]")

        self.df = self.df.sort_values(
            ["company_id", "date"]
        )

    # -------------------------------------------------

    def engineer_daily_return(self):

        self.df["daily_return_pct"] = (
            self.df.groupby("company_id")["adjusted_close"]
            .pct_change() * 100
        )

    # -------------------------------------------------

    def engineer_moving_average(self):

        self.df["ma_20"] = (
            self.df.groupby("company_id")["adjusted_close"]
            .transform(
                lambda x: x.rolling(20).mean()
            )
        )

        self.df["ma_50"] = (
            self.df.groupby("company_id")["adjusted_close"]
            .transform(
                lambda x: x.rolling(50).mean()
            )
        )

    # -------------------------------------------------

    def engineer_volatility(self):

        self.df["volatility_20"] = (
            self.df.groupby("company_id")["daily_return_pct"]
            .transform(
                lambda x: x.rolling(20).std()
            )
        )

    # -------------------------------------------------

    def engineer_price_range(self):

        self.df["price_range"] = (
            self.df["high_price"] -
            self.df["low_price"]
        )

    # -------------------------------------------------

    def engineer_average_volume(self):

        self.df["avg_volume_20"] = (
            self.df.groupby("company_id")["volume"]
            .transform(
                lambda x: x.rolling(20).mean()
            )
        )

    # -------------------------------------------------

    def run(self):

        self.engineer_daily_return()

        self.engineer_moving_average()

        self.engineer_volatility()

        self.engineer_price_range()

        self.engineer_average_volume()

        return self.df