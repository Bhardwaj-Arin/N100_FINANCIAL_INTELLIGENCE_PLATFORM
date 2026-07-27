from src.database.database import DatabaseManager

db = DatabaseManager()

print("=" * 60)
print("DATABASE TEST")
print("=" * 60)

print("\nDatabase Path:")
print(db.db_path)

print("\nExisting Tables:")
print(db.get_table_names())

print("=" * 60)