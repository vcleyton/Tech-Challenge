from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from src.services.books_service import BooksService

stats_bp = Blueprint('stats', __name__)

service = BooksService()

@stats_bp.route('/overview', methods=['GET'])
@jwt_required()
def getStatsOverview():
    stats = service.get_stats_overview()
    return jsonify(stats)

@stats_bp.route('/categories', methods=['GET'])
@jwt_required()
def getStatsByCategory():
    stats = service.get_stats_by_category()
    return jsonify(stats)