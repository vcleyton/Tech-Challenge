from flask import Blueprint, jsonify
from api.database import get_db_connection

stats_bp = Blueprint("stats", __name__, url_prefix="/api/v1/stats")


@stats_bp.route("/overview", methods=["GET"])
def stats_overview():
    """
    Estatísticas gerais da coleção
    ---
    tags:
      - Stats
    responses:
      200:
        description: Estatísticas gerais
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    total_books = cursor.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    avg_price = cursor.execute(
        "SELECT ROUND(AVG(price), 2) FROM books"
    ).fetchone()[0]

    ratings = cursor.execute("""
        SELECT rating, COUNT(*) as total
        FROM books
        GROUP BY rating
        ORDER BY rating
    """).fetchall()

    conn.close()

    return jsonify({
        "total_books": total_books,
        "average_price": avg_price,
        "ratings_distribution": [
            {"rating": r["rating"], "total": r["total"]}
            for r in ratings
        ]
    })

@stats_bp.route("/categories", methods=["GET"])
def stats_by_category():
    """
    Estatísticas detalhadas por categoria
    ---
    tags:
      - Stats
    responses:
      200:
        description: Estatísticas por categoria
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    data = cursor.execute("""
        SELECT
            category,
            COUNT(*) as total_books,
            ROUND(AVG(price), 2) as avg_price,
            MIN(price) as min_price,
            MAX(price) as max_price
        FROM books
        GROUP BY category
        ORDER BY category
    """).fetchall()

    conn.close()

    return jsonify([
        {
            "category": row["category"],
            "total_books": row["total_books"],
            "average_price": row["avg_price"],
            "min_price": row["min_price"],
            "max_price": row["max_price"]
        }
        for row in data
    ])
