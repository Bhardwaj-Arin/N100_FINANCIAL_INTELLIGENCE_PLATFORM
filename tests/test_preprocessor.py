from src.data_ingestion.loader import DataLoader
from src.preprocessing.preprocessor import DataPreprocessor

loader = DataLoader()

datasets = loader.load_all()

processor = DataPreprocessor()

print("=" * 70)
print("PREPROCESSOR TEST")
print("=" * 70)

for name, df in datasets.items():

    cleaned = processor.preprocess(df)

    print()

    print(name.upper())

    print("Original :", df.shape)

    print("Processed:", cleaned.shape)

print("\nAll datasets processed successfully.")