from src.repository.books_repository import BooksRepository
from src.utils.validators import Validator
from src.utils.exceptions import NotFoundError, ValidationError


class BooksService:
    def __init__(self):
        self.repository = BooksRepository()

    def get_all_books(self):
        """
        Retorna todos os livros disponíveis.
        
        Returns:
            list: Lista de dicionários com informações dos livros
        """
        books = self.repository.get_books()
        if not books:
            return []
        return books

    def get_book_by_id(self, book_id):
        """
        Retorna um livro específico pelo ID.
        
        Args:
            book_id (int): ID do livro
            
        Returns:
            dict: Dicionário com informações do livro
            
        Raises:
            ValidationError: Se o book_id for inválido
            NotFoundError: Se o livro não for encontrado
        """
        try:
            Validator.validate_book_id(book_id)
        except ValidationError as e:
            raise ValidationError(str(e))
        
        book = self.repository.get_book_by_id(book_id)
        
        if not book:
            raise NotFoundError(f"Livro com ID {book_id} não encontrado")
        
        return book

    def search_books(self, title=None, min_price=None, max_price=None, rating=None, min_rating=None, max_rating=None, category=None):
        """
        Busca livros com filtros opcionais.
        
        Args:
            title (str, optional): Título ou parte do título do livro
            min_price (float, optional): Preço mínimo
            max_price (float, optional): Preço máximo
            rating (str, optional): Avaliação específica
            min_rating (int, optional): Avaliação mínima
            max_rating (int, optional): Avaliação máxima
            category (str, optional): Categoria do livro
            
        Returns:
            list: Lista de livros que correspondem aos critérios de busca
            
        Raises:
            ValidationError: Se algum dos parâmetros for inválido
        """
        # Valida parâmetros numéricos
        try:
            if min_price is not None:
                Validator.validate_price(min_price)
            if max_price is not None:
                Validator.validate_price(max_price)
            if min_rating is not None:
                if not isinstance(min_rating, int) or min_rating < 0 or min_rating > 5:
                    raise ValidationError("min_rating deve estar entre 0 e 5")
            if max_rating is not None:
                if not isinstance(max_rating, int) or max_rating < 0 or max_rating > 5:
                    raise ValidationError("max_rating deve estar entre 0 e 5")
        except ValidationError as e:
            raise e
        
        # Valida consistência de preços
        if min_price is not None and max_price is not None:
            if float(min_price) > float(max_price):
                raise ValidationError("min_price não pode ser maior que max_price")
        
        # Valida consistência de ratings
        if min_rating is not None and max_rating is not None:
            if min_rating > max_rating:
                raise ValidationError("min_rating não pode ser maior que max_rating")
        
        books = self.repository.search_books(title, min_price, max_price, rating, min_rating, max_rating, category)
        return books if books else []

    def get_categories(self):
        """
        Retorna todas as categorias de livros disponíveis.
        
        Returns:
            list: Lista de categorias únicas
        """
        categories = self.repository.get_categories()
        return categories if categories else []

    def get_stats_overview(self):
        """
        Retorna estatísticas gerais dos livros.
        
        Returns:
            dict: Dicionário com total de livros, preço médio e distribuição de ratings
        """
        return self.repository.get_stats_overview()

    def get_stats_by_category(self):
        """
        Retorna estatísticas agrupadas por categoria.
        
        Returns:
            list: Lista de dicionários com estatísticas por categoria
        """
        return self.repository.get_stats_by_category()