import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Float, cast, Integer, func

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(String)
    stock = Column(Integer)
    rating = Column(String)
    category = Column(String)
    image_url = Column(String)

class BooksService:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'books.db')
        db_url = f"sqlite:///{db_path}"
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.Session = sessionmaker(bind=self.engine)

    def get_books(self):
        session = self.Session()
        try:
            books = session.query(Book).all()
            return [
                {
                    "id": book.id,
                    "title": book.title,
                    "price": book.price,
                    "stock": book.stock,
                    "rating": book.rating,
                    "category": book.category,
                    "image_url": book.image_url
                }
                for book in books
            ]
        finally:
            session.close()

    def get_book_by_id(self, book_id):
        session = self.Session()
        try:
            book = session.query(Book).filter(Book.id == book_id).first()

            if book:
                return {
                    "id": book.id,
                    "title": book.title,
                    "price": book.price,
                    "stock": book.stock,
                    "rating": book.rating,
                    "category": book.category,
                    "image_url": book.image_url
                }
            else:
                return None
        finally:
            session.close()

    def search_books(self, title=None, min_price=None, max_price=None, rating=None, min_rating=None, max_rating=None, category=None):
        session = self.Session()
        try:
            query = session.query(Book)

            if title:
                query = query.filter(Book.title.ilike(f"%{title}%"))
            if min_price is not None:
                query = query.filter(cast(Book.price, Float) >= min_price)
            if max_price is not None:
                query = query.filter(cast(Book.price, Float) <= max_price)
            if rating:
                query = query.filter(Book.rating == rating)
            if min_rating is not None:
                query = query.filter(cast(Book.rating, Integer) >= min_rating)
            if max_rating is not None:
                query = query.filter(cast(Book.rating, Integer) <= max_rating)
            if category:
                query = query.filter(Book.category.ilike(f"%{category}%"))

            results = query.all()

            return [
                {
                    "id": book.id,
                    "title": book.title,
                    "price": book.price,
                    "stock": book.stock,
                    "rating": book.rating,
                    "category": book.category,
                    "image_url": book.image_url
                }
                for book in results
            ]
        finally:
            session.close()

    def get_categories(self):
        session = self.Session()
        try:
            categories = session.query(Book.category).distinct().all()
            return [category[0] for category in categories]
        finally:
            session.close()

    def get_stats_overview(self):
        session = self.Session()
        try:
            total_books = session.query(Book).count()
            avg_price = session.query(func.avg(cast(Book.price, Float))).scalar()
            raw_distribution = session.query(Book.rating, func.count(Book.id)).group_by(Book.rating).all()
            distribution_rating = [{"rating": rating, "count": count} for rating, count in raw_distribution]

            return {
                "total_books": total_books,
                "average_price": round(avg_price, 2),
                "distribution_rating": distribution_rating
            }
        finally:
            session.close()

    def get_stats_by_category(self):
        session = self.Session()
        try:
            raw_stats = session.query(
                Book.category,
                func.count(Book.id),
                func.avg(cast(Book.price, Float))
            ).group_by(Book.category).all()

            stats = [
                {
                    "category": category,
                    "total_books": total_books,
                    "average_price": round(average_price, 2)
                }
                for category, total_books, average_price in raw_stats
            ]

            return stats
        finally:
            session.close()