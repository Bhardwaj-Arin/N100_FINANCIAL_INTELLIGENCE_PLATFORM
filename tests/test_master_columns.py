from src.database.database import DatabaseManager

db = DatabaseManager()

tables = [
    "company_features",
    "financial_ratio_features",
    "market_features",
    "sector_features"
]

for table in tables:

    print("\n" + "="*60)
    print(table)
    print("="*60)

    df = db.read_table(table)

    print(df.columns.tolist())