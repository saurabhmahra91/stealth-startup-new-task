import os
from pathlib import Path

products_sqlite = Path(os.environ.get("PRODUCTS_SQLITE3_DB_PATH", "../db.sqlite3"))
products_table = os.environ.get("PRODUCTS_TABLE_NAME", "fashion_products")
