"""
Rotas de livros - Busca, listagem e detalhes de livros.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.services.books_service import BooksService
from src.utils.exceptions import ValidationError, NotFoundError

books_bp = Blueprint('books', __name__)

service = BooksService()

@books_bp.route('', methods=['GET'])
def get_all_books():
    """
    Retorna todos os livros disponíveis.
    
    ---
    tags:
      - Livros
    responses:
      200:
        description: Lista de todos os livros
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              price:
                type: string
              stock:
                type: integer
              rating:
                type: string
              category:
                type: string
              image_url:
                type: string
    """
    try:
        books = service.get_all_books()
        return jsonify(books), 200
    except Exception as e:
        return jsonify({"message": "Erro ao buscar livros", "error": "InternalServerError"}), 500


@books_bp.route('/<int:id>', methods=['GET'])
def get_book_by_id(id):
    """
    Retorna um livro específico pelo ID.
    
    ---
    tags:
      - Livros
    parameters:
      - in: path
        name: id
        type: integer
        required: true
        description: ID do livro
    responses:
      200:
        description: Detalhes do livro
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            price:
              type: string
            stock:
              type: integer
            rating:
              type: string
            category:
              type: string
            image_url:
              type: string
      400:
        description: ID inválido
      404:
        description: Livro não encontrado
    """
    try:
        book = service.get_book_by_id(id)
        return jsonify(book), 200
    except ValidationError as e:
        return jsonify({"message": str(e), "error": "ValidationError"}), 400
    except NotFoundError as e:
        return jsonify({"message": str(e), "error": "NotFoundError"}), 404
    except Exception as e:
        return jsonify({"message": "Erro ao buscar livro", "error": "InternalServerError"}), 500


@books_bp.route('/search', methods=['GET'])
def search_books():
    """
    Busca livros com filtros opcionais.
    
    ---
    tags:
      - Livros
    parameters:
      - in: query
        name: title
        type: string
        description: Título ou parte do título
      - in: query
        name: min_price
        type: number
        description: Preço mínimo
      - in: query
        name: max_price
        type: number
        description: Preço máximo
      - in: query
        name: category
        type: string
        description: Categoria do livro
      - in: query
        name: min_rating
        type: integer
        description: Avaliação mínima (0-5)
      - in: query
        name: max_rating
        type: integer
        description: Avaliação máxima (0-5)
    responses:
      200:
        description: Lista de livros que correspondem aos critérios
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              price:
                type: string
              stock:
                type: integer
              rating:
                type: string
              category:
                type: string
              image_url:
                type: string
      400:
        description: Parâmetros de busca inválidos
    """
    try:
        title = request.args.get('title')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        category = request.args.get('category')
        min_rating = request.args.get('min_rating', type=int)
        max_rating = request.args.get('max_rating', type=int)
        rating = request.args.get('rating')

        books = service.search_books(
            title=title,
            min_price=min_price,
            max_price=max_price,
            rating=rating,
            min_rating=min_rating,
            max_rating=max_rating,
            category=category
        )
        return jsonify(books), 200
    except ValidationError as e:
        return jsonify({"message": str(e), "error": "ValidationError"}), 400
    except Exception as e:
        return jsonify({"message": "Erro ao buscar livros", "error": "InternalServerError"}), 500


@books_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Retorna todas as categorias de livros disponíveis.
    
    ---
    tags:
      - Livros
    responses:
      200:
        description: Lista de categorias únicas
        schema:
          type: array
          items:
            type: string
            description: Nome da categoria
            example: "Fiction"
    """
    try:
        categories = service.get_categories()
        return jsonify(categories), 200
    except Exception as e:
        return jsonify({"message": "Erro ao buscar categorias", "error": "InternalServerError"}), 500



