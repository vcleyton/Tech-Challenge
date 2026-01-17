from flask_restx import Namespace, Resource, fields
from api.database import get_db_connection

api = Namespace("stats", description="Estatísticas gerais e por categoria")

@api.route("/overview")
class StatsOverview(Resource):
    @api.doc(description="Estatísticas gerais da coleção")
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        total_books = cursor.execute(
            "SELECT COUNT(*) FROM books"
        ).fetchone()[0]

        avg_price = cursor.execute(
            "SELECT ROUND(AVG(price), 2) FROM books"
        ).fetchone()[0]

        avg_rating = cursor.execute(
            "SELECT ROUND(AVG(rating), 2) FROM books"
        ).fetchone()[0]

        ratings = cursor.execute("""
            SELECT rating, COUNT(*) as total
            FROM books
            GROUP BY rating
            ORDER BY rating
        """).fetchall()

        conn.close()

        return {
            "total_books": total_books,
            "average_price": avg_price,
            "average_rating": avg_rating,
            "ratings_distribution": [
                {"rating": r["rating"], "total": r["total"]}
                for r in ratings
            ]
        }

@api.route("/categories")
class StatsByCategory(Resource):
    @api.doc(description="Estatísticas detalhadas por categoria")
    def get(self):
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

        return [
            {
                "category": row["category"],
                "total_books": row["total_books"],
                "average_price": row["avg_price"],
                "min_price": row["min_price"],
                "max_price": row["max_price"]
            }
            for row in data
        ]
