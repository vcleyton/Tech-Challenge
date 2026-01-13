"""
Módulo de validadores e utilitários de validação.
Centraliza lógica de validação para ser reutilizada em toda a aplicação.
"""

import re
from src.utils.exceptions import ValidationError


class Validator:
    """Classe com métodos estáticos para validação de dados."""

    @staticmethod
    def validate_username(username):
        """
        Valida o nome de usuário.
        
        Args:
            username (str): Nome de usuário a validar
            
        Raises:
            ValidationError: Se o username for inválido
        """
        if not username or not isinstance(username, str):
            raise ValidationError("Username deve ser uma string não vazia")
        
        if len(username) < 3:
            raise ValidationError("Username deve ter pelo menos 3 caracteres")
        
        if len(username) > 50:
            raise ValidationError("Username não pode exceder 50 caracteres")
        
        if not re.match("^[a-zA-Z0-9_-]+$", username):
            raise ValidationError("Username pode conter apenas letras, números, underscore e hífen")
        
        return True

    @staticmethod
    def validate_password(password):
        """
        Valida a senha.
        
        Args:
            password (str): Senha a validar
            
        Raises:
            ValidationError: Se a senha for inválida
        """
        if not password or not isinstance(password, str):
            raise ValidationError("Password deve ser uma string não vazia")
        
        if len(password) < 6:
            raise ValidationError("Password deve ter pelo menos 6 caracteres")
        
        if len(password) > 128:
            raise ValidationError("Password não pode exceder 128 caracteres")
        
        return True

    @staticmethod
    def validate_book_id(book_id):
        """
        Valida o ID do livro.
        
        Args:
            book_id: ID do livro a validar
            
        Raises:
            ValidationError: Se o book_id for inválido
        """
        if not isinstance(book_id, int) or book_id <= 0:
            raise ValidationError("Book ID deve ser um inteiro positivo")
        
        return True

    @staticmethod
    def validate_price(price):
        """
        Valida o preço.
        
        Args:
            price: Preço a validar
            
        Raises:
            ValidationError: Se o preço for inválido
        """
        try:
            price_float = float(price)
            if price_float < 0:
                raise ValidationError("Preço não pode ser negativo")
            return True
        except (TypeError, ValueError):
            raise ValidationError("Preço deve ser um número válido")

    @staticmethod
    def validate_rating(rating):
        """
        Valida a avaliação (rating).
        
        Args:
            rating: Avaliação a validar
            
        Raises:
            ValidationError: Se a avaliação for inválida
        """
        try:
            rating_int = int(rating)
            if rating_int < 0 or rating_int > 5:
                raise ValidationError("Rating deve estar entre 0 e 5")
            return True
        except (TypeError, ValueError):
            raise ValidationError("Rating deve ser um inteiro entre 0 e 5")

    @staticmethod
    def validate_stock(stock):
        """
        Valida o estoque.
        
        Args:
            stock: Estoque a validar
            
        Raises:
            ValidationError: Se o estoque for inválido
        """
        try:
            stock_int = int(stock)
            if stock_int < 0:
                raise ValidationError("Stock não pode ser negativo")
            return True
        except (TypeError, ValueError):
            raise ValidationError("Stock deve ser um inteiro não negativo")

    @staticmethod
    def validate_prediction_input(data, valid_categories=None):
        """
        Valida os dados de entrada para predição de ML.
        
        Args:
            data (dict): Dados a validar
            valid_categories (list, optional): Lista de categorias válidas do banco de dados
            
        Raises:
            ValidationError: Se os dados forem inválidos
        """
        required_fields = ['category', 'stock', 'rating']
        
        for field in required_fields:
            if field not in data or data[field] is None:
                raise ValidationError(f"Campo obrigatório '{field}' está faltando")
        
        try:
            Validator.validate_stock(data['stock'])
            Validator.validate_rating(data['rating'])
        except ValidationError as e:
            raise e
        
        if not isinstance(data['category'], str) or len(data['category'].strip()) == 0:
            raise ValidationError("Category deve ser uma string não vazia")
        
        if valid_categories is not None:
            if data['category'].lower().strip() not in valid_categories:
                raise ValidationError(f"Categoria '{data['category']}' não existe. Categorias válidas: {', '.join(valid_categories)}")
        
        return True
