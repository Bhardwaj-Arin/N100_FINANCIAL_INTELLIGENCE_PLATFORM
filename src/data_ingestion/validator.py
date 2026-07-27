"""
validator.py
---------------------------------
This module validates the raw dataset before any cleaning or preprocessing.

Author : Your Name
Project: Intelligent Customer Analytics Platform
"""

from pathlib import Path
import pandas as pd


class DataValidator:
    """
    Validates the integrity and structure of the dataset.
    """

    REQUIRED_COLUMNS = [
        "Invoice",
        "StockCode",
        "Description",
        "Quantity",
        "InvoiceDate",
        "Price",
        "Customer ID",
        "Country",
    ]

    def __init__(self, dataframe: pd.DataFrame, file_path: str | Path):
        """
        Parameters
        ----------
        dataframe : pd.DataFrame
            Loaded dataset.
        file_path : str | Path
            Path to the original CSV file.
        """
        self.df = dataframe
        self.file_path = Path(file_path)

    def validate_file_exists(self):
        """Check whether the source file exists."""
        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found at:\n{self.file_path}"
            )

    def validate_not_empty(self):
        """Check whether dataframe contains data."""
        if self.df.empty:
            raise ValueError("Dataset is empty.")

    def validate_required_columns(self):
        """Ensure all required columns exist."""
        missing = [
            col for col in self.REQUIRED_COLUMNS
            if col not in self.df.columns
        ]

        if missing:
            raise ValueError(
                f"Missing required columns:\n{missing}"
            )

    def validate_duplicate_columns(self):
        """Check duplicate column names."""
        duplicates = self.df.columns[self.df.columns.duplicated()]

        if len(duplicates) > 0:
            raise ValueError(
                f"Duplicate column names found:\n{duplicates.tolist()}"
            )

    def validate_numeric_columns(self):
        """Ensure numeric columns are numeric."""
        numeric_columns = [
            "Quantity",
            "Price",
            "Customer ID",
        ]

        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(self.df[col]):
                print(f"Warning: '{col}' is not numeric.")

    def validation_summary(self):
        """Print validation statistics."""

        print("=" * 60)
        print("DATA VALIDATION SUMMARY")
        print("=" * 60)

        print(f"Rows              : {len(self.df):,}")
        print(f"Columns           : {self.df.shape[1]}")

        print("\nMissing Values (%)")

        missing = (
            self.df.isnull()
            .mean()
            .mul(100)
            .round(2)
        )

        print(missing)

        print("\nDuplicate Rows")

        print(self.df.duplicated().sum())

        print("\nNegative Quantity")

        print((self.df["Quantity"] < 0).sum())

        print("\nNegative Price")

        print((self.df["Price"] < 0).sum())

        print("=" * 60)

    def validate(self):
        """
        Run all validation checks.
        """

        self.validate_file_exists()
        self.validate_not_empty()
        self.validate_required_columns()
        self.validate_duplicate_columns()
        self.validate_numeric_columns()

        print("All validation checks passed.\n")