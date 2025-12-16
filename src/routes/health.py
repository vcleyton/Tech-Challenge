from flask import Blueprint, jsonify
from src.services.books_service import BooksService

health_bp = Blueprint('health', __name__)

service = BooksService()

@health_bp.route('/', methods=['GET'])
def healthCheck():
    return jsonify({"status": "OK"})