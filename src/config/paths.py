from pathlib import Path

# Root folder
ROOT_DIR = Path(__file__).resolve().parents[2]

# Data folders
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Database
DB_DIR = ROOT_DIR / "db"
DATABASE_PATH = DB_DIR / "nifty100.db"

# Output
OUTPUT_DIR = ROOT_DIR / "output"

# Reports
REPORTS_DIR = ROOT_DIR / "reports"

# Docs
DOCS_DIR = ROOT_DIR / "docs"