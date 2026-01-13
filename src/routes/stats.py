"""
Rotas de estatísticas - Dados estatísticos sobre livros e categorias.
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.services.books_service import BooksService

stats_bp = Blueprint('stats', __name__)

service = BooksService()

@stats_bp.route('/overview', methods=['GET'])
def get_stats_overview():
    """
    Retorna estatísticas gerais sobre os livros.
    
    ---
    tags:
      - Estatísticas
    responses:
      200:
        description: Estatísticas gerais
        schema:
          type: object
          properties:
            total_books:
              type: integer
              description: Total de livros na base de dados
            average_price:
              type: number
              description: Preço médio dos livros
            distribution_rating:
              type: array
              items:
                type: object
                properties:
                  rating:
                    type: string
                    description: Valor da avaliação
                  count:
                    type: integer
                    description: Quantidade de livros com essa avaliação
    """
    try:
        stats = service.get_stats_overview()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"message": "Erro ao buscar estatísticas", "error": "InternalServerError"}), 500


@stats_bp.route('/categories', methods=['GET'])
def get_stats_by_category():
    """
    Retorna estatísticas agrupadas por categoria.
    
    ---
    tags:
      - Estatísticas
    responses:
      200:
        description: Estatísticas por categoria
        schema:
          type: array
          items:
            type: object
            properties:
              category:
                type: string
                description: Nome da categoria
              total_books:
                type: integer
                description: Total de livros nessa categoria
              average_price:
                type: number
                description: Preço médio dos livros nessa categoria
    """
    try:
        stats = service.get_stats_by_category()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"message": "Erro ao buscar estatísticas", "error": "InternalServerError"}), 500
