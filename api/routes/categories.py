from flask_restx import Namespace, Resource
from api.database import get_db_connection

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
