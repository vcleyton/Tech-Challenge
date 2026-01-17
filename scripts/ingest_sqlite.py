"""
Script de ingestão de dados:
- Lê o arquivo CSV com os livros
- Cria um banco SQLite
- Cria a tabela books
- Insere os dados no banco

"""

from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CSV_PATH = DATA_DIR / "books.csv"
DB_PATH = DATA_DIR / "books.db"


def create_connection(db_path: Path):
    """
    Cria conexão com o banco SQLite.
    Se o arquivo não existir, ele será criado automaticamente.
    """
    conn = sqlite3.connect(db_path)
    return conn


def create_table(conn: sqlite3.Connection):
    """
    Cria a tabela books no banco de dados.
    Remove a tabela se já existir para evitar duplicação.
    """
    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS books
    """)

    cursor.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            rating INTEGER,
            availability TEXT,
            category TEXT,
            image_url TEXT,
            product_url TEXT
        )
    """)

    conn.commit()


def clean_price_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrige possíveis problemas de encoding no preço.
    Exemplo: 'Â12.29' -> '12.29'
    """
    df["price"] = (
        df["price"]
        .astype(str)
        .str.replace("Â", "", regex=False)
        .astype(float)
    )
    return df


def insert_data(conn: sqlite3.Connection, df: pd.DataFrame):
    """
    Insere os dados do DataFrame na tabela SQLite.
    """
    df.to_sql(
        "books",
        conn,
        if_exists="append",
        index=False
    )


def main():
    print("Iniciando ingestão dos dados no SQLite...")

    if not CSV_PATH.exists():
        raise FileNotFoundError("Arquivo books.csv não encontrado.")

    # Lê o CSV
    df = pd.read_csv(CSV_PATH)

    # Corrige a coluna de preço
    df = clean_price_column(df)

    # Cria conexão com o banco
    conn = create_connection(DB_PATH)

    # Cria a tabela
    create_table(conn)

    # Insere os dados
    insert_data(conn, df)

    conn.close()

    print(f"Ingestão finalizada com sucesso! Banco criado em {DB_PATH}")


if __name__ == "__main__":
    main()
