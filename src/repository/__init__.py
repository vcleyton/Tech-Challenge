"""
Módulo de repositórios da aplicação.
Define classes para acesso aos dados (Data Access Layer).
"""

from .user_repository import UserRepository
from .books_repository import BooksRepository

__all__ = ['UserRepository', 'BooksRepository']
