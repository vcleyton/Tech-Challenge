from flask import Blueprint, jsonify
from src.services.books_service import BooksService

stats_bp = Blueprint('stats', __name__)

service = BooksService()

@stats_bp.route('/overview', methods=['GET'])
def getStatsOverview():
    stats = service.get_stats_overview()
    return jsonify(stats)

@stats_bp.route('/categories', methods=['GET'])
def getStatsByCategory():
    stats = service.get_stats_by_category()
    return jsonify(stats)