from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

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
