import sqlite3

DB_PATH = "data/books.db"


def get_db_connection():
    """
    Cria e retorna uma conexão com o banco SQLite.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conn
