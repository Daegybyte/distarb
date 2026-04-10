"""
One-time migration script to seed the SQLite database from stock_list.csv.
Run once from the app/ directory: python migrate.py
"""

import sqlite3
from pathlib import Path

import pandas as pd

base_path = Path(__file__).parent
csv_path = (base_path / "src/stock_list.csv").resolve()
db_path = (base_path / "src/distarb.db").resolve()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop and recreate to ensure clean schema
cursor.execute("DROP TABLE IF EXISTS stocks")
cursor.execute(
    """
    CREATE TABLE stocks (
        ticker_symbol TEXT PRIMARY KEY,
        company_name TEXT NOT NULL,
        clean_company TEXT NOT NULL,
        ticker_lower TEXT NOT NULL
    )
"""
)

df = pd.read_csv(csv_path)
df = df.rename(columns={"clean_companies": "clean_company", "tickers_lower": "ticker_lower"})
df = df.dropna()  # drop rows with any null values


for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO stocks VALUES (?, ?, ?, ?)",
        (row["ticker_symbol"], row["company_name"], row["clean_company"], row["ticker_lower"]),
    )

conn.commit()
conn.close()

print(f"Migration complete. Database created at {db_path}")
print(f"Rows inserted: {len(df)}")
