"""
Rota de health check - Verifica o status da aplicação.
"""

from flask import Blueprint, jsonify
from src.services.books_service import BooksService

health_bp = Blueprint('health', __name__)

service = BooksService()

@health_bp.route('/', methods=['GET'])
def health_check():
    """
    Verifica o status de saúde da aplicação.
    
    ---
    tags:
      - Health
    responses:
      200:
        description: Aplicação está funcionando
        schema:
          type: object
          properties:
            status:
              type: string
              example: "OK"
    """
    return jsonify({"status": "OK"}), 200
