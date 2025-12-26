from flask_restx import Namespace, Resource
from api.database import get_db_connection
from flask import Blueprint, jsonify

api = Namespace("categories", description="Categorias de livros")


@api.route("/")
class CategoryList(Resource):
    def get(self):
        """
        Lista todas as categorias disponíveis.
        """
        conn = get_db_connection()
        categories = conn.execute(
            "SELECT DISTINCT category FROM books"
        ).fetchall()
        conn.close()

        return [row["category"] for row in categories]


categories_bp = Blueprint("categories", __name__, url_prefix="/api/v1/categories")


@categories_bp.route("/ranking", methods=["GET"])
def categories_ranking():
    conn = get_db_connection()
    result = conn.execute("""
        SELECT category, COUNT(*) AS total
        FROM books
        GROUP BY category
        ORDER BY total DESC
    """).fetchall()
    conn.close()

    return jsonify([dict(row) for row in result])
