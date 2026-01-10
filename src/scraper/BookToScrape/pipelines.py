# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import os

class BooktoscrapePipeline:
    def open_spider(self, spider):
        # DB file created in current working dir (where you run `scrapy crawl`)
        db_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'instance'))
        os.makedirs(db_dir, exist_ok=True)
        db_path = os.path.join(db_dir, "books.db")

        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price REAL,
                stock INTEGER,
                rating INTEGER,
                category TEXT,
                image_url TEXT
            )
            """
        )
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        self.cur.execute(
            """
            INSERT INTO books (title, price, stock, rating, category, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                adapter.get("title"),
                adapter.get("price"),
                adapter.get("stock"),
                adapter.get("rating"),
                adapter.get("category"),
                adapter.get("image_url"),
            ),
        )
        self.conn.commit()
        return item
