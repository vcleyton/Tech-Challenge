from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import pandas as pd


@dataclass(frozen=True)
class DataStoreConfig:
    csv_path: Path


class DataStore:

    def __init__(self, config: DataStoreConfig):
        self.config = config

    def csv_exists(self) -> bool:
        return self.config.csv_path.exists()

    def load_books_df(self) -> pd.DataFrame:
        if not self.csv_exists():
            raise FileNotFoundError(f"Arquivo inexistente: {self.config.csv_path}")
        df = pd.read_csv(self.config.csv_path)
        return df

    def ping(self) -> dict:
        if not self.csv_exists():
            return {
                "status": "degraded",
                "data_source": "csv",
                "csv_path": str(self.config.csv_path),
                "message": "Necessario rodar o script de scraping",
            }

        try:
            df = self.load_books_df()
            return {
                "status": "ok",
                "data_source": "csv",
                "csv_path": str(self.config.csv_path),
                "rows": int(df.shape[0]),
                "columns": list(df.columns),
            }
        except Exception as e:
            return {
                "status": "down",
                "data_source": "csv",
                "csv_path": str(self.config.csv_path),
                "error": str(e),
            }
        
    def list_books(self):
        df = self.load_books_df().copy()

        if "id" not in df.columns:
            df.insert(0, "id", range(len(df)))

        return df.to_dict(orient="records")

    def get_book_by_id(self, book_id: int):
        df = self.load_books_df().copy()

        if "id" not in df.columns:
            df.insert(0, "id", range(len(df)))

        row = df[df["id"] == book_id]
        if row.empty:
            return None
        return row.iloc[0].to_dict()

    def search_books(self, title: Optional[str] = None, category: Optional[str] = None):
        df = self.load_books_df().copy()

        if "id" not in df.columns:
            df.insert(0, "id", range(len(df)))

        if title:
            df = df[df["title"].str.contains(title, case=False, na=False)]

        if category:
            df = df[df["category"].str.contains(category, case=False, na=False)]

        return df.to_dict(orient="records")

    def list_categories(self):
        df = self.load_books_df()
        cats = sorted(df["category"].dropna().unique().tolist())
        return cats

# def default_data_store() -> DataStore:
#     csv_path = Path("data/processed/books.csv")
#     return DataStore(DataStoreConfig(csv_path=csv_path))

def default_data_store() -> DataStore:
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "data" / "processed" / "books.csv"
    return DataStore(DataStoreConfig(csv_path=csv_path))