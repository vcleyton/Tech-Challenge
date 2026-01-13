"""
Módulo de serviços da aplicação.
Define classes de lógica de negócio (Business Logic Layer).
"""

from .auth_service import AuthService
from .books_service import BooksService
from .ml_service import MLService

__all__ = ['AuthService', 'BooksService', 'MLService']
