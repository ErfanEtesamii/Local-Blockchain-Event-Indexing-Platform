import os
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://indexer_user:indexer@localhost:5432/blockchain_indexer"
)

def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)