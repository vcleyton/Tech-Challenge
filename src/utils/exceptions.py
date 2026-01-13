"""
Módulo de exceções personalizadas da aplicação.
Centraliza todas as exceções customizadas para tratamento consistente de erros.
"""

class ValidationError(Exception):
    """Exceção levantada quando a validação de dados falha."""
    pass


class NotFoundError(Exception):
    """Exceção levantada quando um recurso não é encontrado."""
    pass


class UnauthorizedError(Exception):
    """Exceção levantada quando o usuário não está autorizado."""
    pass


class ConflictError(Exception):
    """Exceção levantada quando há um conflito de dados (ex: usuário duplicado)."""
    pass


class DatabaseError(Exception):
    """Exceção levantada quando há erro na operação do banco de dados."""
    pass


class MLError(Exception):
    """Exceção levantada quando há erro no módulo de Machine Learning."""
    pass
