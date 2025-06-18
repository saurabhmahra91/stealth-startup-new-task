import logging
import sqlite3

from .constants import products_sqlite
from ..memory import valkey_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_db_status():
    logging.info("products path -- %s", str(products_sqlite.resolve()))
    if not products_sqlite.exists():
        logger.warning(f"Database file not found at: {products_sqlite.resolve()}")
        return
    logger.info(f"Database file found at: {products_sqlite.resolve()}")

    try:
        conn = sqlite3.connect(products_sqlite)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            table_names = [t[0] for t in tables]
            logger.info(f"Tables in database: {table_names}")
        else:
            logger.info("No tables found in the database.")
        conn.close()
    except Exception as e:
        logger.error(f"Error while accessing the database: {e}")
