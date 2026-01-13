"""
Módulo de utilitários da aplicação.
Contém funções auxiliares, validadores e exceções.
"""

from .exceptions import (
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ConflictError,
    DatabaseError,
    MLError
)
from .validators import Validator

__all__ = [
    'ValidationError',
    'NotFoundError',
    'UnauthorizedError',
    'ConflictError',
    'DatabaseError',
    'MLError',
    'Validator'
]
