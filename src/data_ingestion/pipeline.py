from src.data_ingestion.loader import DataLoader
from src.database.database import DatabaseManager


class ETLPipeline:
    """
    End-to-End ETL Pipeline

    Steps:
    1. Load datasets
    2. Save into SQLite
    """

    def __init__(self):
        self.loader = DataLoader()
        self.database = DatabaseManager()

    def run(self):

        print("=" * 60)
        print("STARTING ETL PIPELINE")
        print("=" * 60)

        # -------------------------
        # Load datasets
        # -------------------------

        datasets = self.loader.load_all()

        print("\nDatasets Loaded Successfully\n")

        # -------------------------
        # Save into database
        # -------------------------

        for table_name, dataframe in datasets.items():

            self.database.create_table(
                dataframe=dataframe,
                table_name=table_name
            )

            print(
                f"✓ {table_name:20}"
                f" -> {len(dataframe):,} rows"
            )

        print("\nETL COMPLETED SUCCESSFULLY")

        print("\nTables Available")

        print(self.database.get_table_names())