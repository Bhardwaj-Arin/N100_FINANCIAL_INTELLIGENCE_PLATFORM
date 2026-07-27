from src.database.database import DatabaseManager

db = DatabaseManager()

df = db.read_table("companies")

print(df.head(15))
print()
print(df.columns.tolist())