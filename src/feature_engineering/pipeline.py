"""
Feature Engineering Pipeline
"""

import pandas as pd

from src.database.database import DatabaseManager

from src.feature_engineering.ratio_features import FinancialRatioEngineer
from src.feature_engineering.market_features import MarketFeatureEngineer
from src.feature_engineering.price_features import PriceFeatureEngineer
from src.feature_engineering.sector_features import SectorFeatureEngineer
from src.feature_engineering.company_features import CompanyFeatureEngineer

from src.config.paths import PROCESSED_DATA_DIR


class FeatureEngineeringPipeline:

    def __init__(self):

        self.db = DatabaseManager()

    # -------------------------------------------------

    def run_ratio_features(self):

        print("\nRunning Financial Ratio Feature Engineering...")

        df = self.db.read_table("financial_ratios")

        result = FinancialRatioEngineer(df).run()

        self.db.create_table(
            result,
            "financial_ratio_features"
        )

        print("✓ Financial Ratio Features Completed")

    # -------------------------------------------------

    def run_market_features(self):

        print("\nRunning Market Feature Engineering...")

        df = self.db.read_table("market_cap")

        result = MarketFeatureEngineer(df).run()

        self.db.create_table(
            result,
            "market_features"
        )

        print("✓ Market Features Completed")

    # -------------------------------------------------

    def run_price_features(self):

        print("\nRunning Price Feature Engineering...")

        df = self.db.read_table("stock_prices")

        result = PriceFeatureEngineer(df).run()

        self.db.create_table(
            result,
            "price_features"
        )

        print("✓ Price Features Completed")

    # -------------------------------------------------

    def run_sector_features(self):

        print("\nRunning Sector Feature Engineering...")

        df = self.db.read_table("sectors")

        result = SectorFeatureEngineer(df).run()

        self.db.create_table(
            result,
            "sector_features"
        )

        print("✓ Sector Features Completed")

    # -------------------------------------------------

    def run_company_features(self):

        print("\nRunning Company Feature Engineering...")

        df = self.db.read_table("companies")

        result = CompanyFeatureEngineer(df).run()

        self.db.create_table(
            result,
            "company_features"
        )

        print("✓ Company Features Completed")

    # -------------------------------------------------

    def build_master_dataset(self):

        print("\nBuilding Master Feature Dataset...")

        company = self.db.read_table("company_features")

        ratio = self.db.read_table("financial_ratio_features")

        market = self.db.read_table("market_features")

        sector = self.db.read_table("sector_features")

        master = company.copy()

        if "company_id" in ratio.columns:
            master = master.merge(
                ratio,
                on="company_id",
                how="left"
            )

        if "company_id" in market.columns:
            master = master.merge(
                market,
                on="company_id",
                how="left"
            )

        if "company_id" in sector.columns:
            master = master.merge(
                sector,
                on="company_id",
                how="left"
            )

        master.to_csv(
            PROCESSED_DATA_DIR / "master_features.csv",
            index=False
        )

        self.db.create_table(
            master,
            "master_features"
        )

        print("✓ Master Dataset Saved")

        print(f"Rows : {master.shape[0]}")
        print(f"Cols : {master.shape[1]}")

    # -------------------------------------------------

    def run(self):

        self.run_ratio_features()

        self.run_market_features()

        self.run_price_features()

        self.run_sector_features()

        self.run_company_features()

        self.build_master_dataset()

        print("\nAll Feature Engineering Modules Completed Successfully.")