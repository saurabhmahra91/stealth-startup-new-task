import csv
import sqlite3
from pathlib import Path


def ingest_fashion_products(csv_path: Path, db_path: Path):
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        columns = [col.strip().replace(" ", "_").replace("(", "").replace(")", "") for col in headers]
        rows = [row for row in reader]

    conn: sqlite3.Connection = sqlite3.connect(db_path)
    cursor: sqlite3.Cursor = conn.cursor()

    # Create table (drop-dead gorgeous table definition)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fashion_products (
            id TEXT PRIMARY KEY,
            name TEXT,
            category TEXT,
            available_sizes TEXT,
            fit TEXT,
            fabric TEXT,
            sleeve_length TEXT,
            color_or_print TEXT,
            occasion TEXT,
            neckline TEXT,
            length TEXT,
            pant_type TEXT,
            usd_price REAL
        )
    """)

    # Purge runway of old data
    cursor.execute("DELETE FROM fashion_products")

    # Insert fresh new looks
    placeholders = ",".join(["?"] * len(columns))
    insert_sql = f"INSERT INTO fashion_products ({','.join(columns)}) VALUES ({placeholders})"
    cursor.executemany(insert_sql, rows)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Swap the file paths below as needed
    ingest_fashion_products(Path("fashion_catalog.csv"), Path("db.sqlite3"))
