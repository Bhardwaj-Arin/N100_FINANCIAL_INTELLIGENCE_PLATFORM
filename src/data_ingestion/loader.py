"""
Data Loader Module
Loads all Excel datasets into memory.
"""

import pandas as pd

from src.config.paths import RAW_DATA_DIR


class DataLoader:
    """
    Loads all project datasets.
    """

    def __init__(self):
        self.datasets = {}

    def load_excel(self, filename):
        """
        Load an Excel file.
        """

        filepath = RAW_DATA_DIR / filename

        # companies.xlsx has its real header on the second row
        if filename == "companies.xlsx":
            return pd.read_excel(filepath, header=1)

        return pd.read_excel(filepath)
    def load_all(self):
        """
        Load every dataset.
        """

        files = [
            "companies.xlsx",
            "analysis.xlsx",
            "balancesheet.xlsx",
            "cashflow.xlsx",
            "documents.xlsx",
            "profitandloss.xlsx",
            "prosandcons.xlsx",
            "financial_ratios.xlsx",
            "market_cap.xlsx",
            "peer_groups.xlsx",
            "sectors.xlsx",
            "stock_prices.xlsx",
        ]

        for file in files:
            name = file.replace(".xlsx", "")
            self.datasets[name] = self.load_excel(file)

        return self.datasets