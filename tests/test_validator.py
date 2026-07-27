from src.data_ingestion.validator import DataValidator

validator = DataValidator()

print("=" * 60)
print("VALIDATION REPORT")
print("=" * 60)

missing = validator.validate_files_exist()
unreadable = validator.validate_excel_readable()
empty = validator.validate_empty_files()

print()

print("Missing Files")
print(missing)

print()

print("Unreadable Files")
print(unreadable)

print()

print("Empty Files")
print(empty)

print("=" * 60)