from src.data_ingestion.loader import DataLoader
from src.preprocessing.cleaner import DataCleaner

loader = DataLoader()
datasets = loader.load_all()

cleaner = DataCleaner()

print("=" * 70)
print("PREPROCESSING TEST")
print("=" * 70)

for name, df in datasets.items():

    cleaned = cleaner.clean(df)

    print(f"\n{name.upper()}")

    print(f"Original Shape : {df.shape}")

    print(f"Cleaned Shape  : {cleaned.shape}")

print("\nCleaning completed successfully.")