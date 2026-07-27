from src.data_ingestion.loader import DataLoader

loader = DataLoader()
datasets = loader.load_all()

for name, df in datasets.items():
    print("=" * 80)
    print(name.upper())
    print("=" * 80)
    print(df.columns.tolist())
    print()