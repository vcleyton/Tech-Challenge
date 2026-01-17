from flask_restx import Namespace, Resource, fields
from flask import request
from api.database import get_db_connection

api = Namespace(
    "books",
    description="Operações relacionadas a livros"
)


book_model = api.model("Book", {
    "id": fields.Integer(description="ID do livro"),
    "title": fields.String(description="Título do livro"),
    "price": fields.Float(description="Preço"),
    "rating": fields.Integer(description="Avaliação (1 a 5)"),
    "availability": fields.String(description="Disponibilidade"),
    "category": fields.String(description="Categoria"),
    "image_url": fields.String(description="URL da imagem"),
    "product_url": fields.String(description="URL do produto")
})


@api.route("/")
class BookList(Resource):
    @api.marshal_list_with(book_model)
    @api.doc(description="Lista todos os livros disponíveis")
    def get(self):
        conn = get_db_connection()
        books = conn.execute("SELECT * FROM books").fetchall()
        conn.close()
        return books


@api.route("/<int:book_id>")
class BookDetail(Resource):
    @api.marshal_with(book_model)
    @api.doc(description="Retorna detalhes de um livro pelo ID")
    def get(self, book_id):
        conn = get_db_connection()
        book = conn.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,)
        ).fetchone()
        conn.close()

        if not book:
            api.abort(404, "Livro não encontrado")

        return book

@api.route("/search")
class BookSearch(Resource):
    @api.marshal_list_with(book_model)
    @api.doc(
        description="Busca livros por filtros",
        params={
            "title": "Parte do título",
            "category": "Categoria",
            "min_price": "Preço mínimo",
            "max_price": "Preço máximo",
            "rating": "Avaliação mínima"
        }
    )
    def get(self):
        title = request.args.get("title")
        category = request.args.get("category")
        min_price = request.args.get("min_price", type=float)
        max_price = request.args.get("max_price", type=float)
        rating = request.args.get("rating", type=int)

        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")

        if category:
            query += " AND category = ?"
            params.append(category)

        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)

        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)

        if rating is not None:
            query += " AND rating >= ?"
            params.append(rating)

        conn = get_db_connection()
        books = conn.execute(query, params).fetchall()
        conn.close()

        return books


@api.route("/top-rated")
class TopRatedBooks(Resource):
    @api.marshal_list_with(book_model)
    @api.doc(
        description="Lista livros com melhor avaliação",
        params={"limit": "Quantidade máxima (default=10)"}
    )
    def get(self):
        limit = request.args.get("limit", default=10, type=int)

        conn = get_db_connection()
        books = conn.execute("""
            SELECT * FROM books
            WHERE rating = 5
            ORDER BY price ASC
            LIMIT ?
        """, (limit,)).fetchall()
        conn.close()

        return books


@api.route("/price-range")
class BooksByPriceRange(Resource):
    @api.marshal_list_with(book_model)
    @api.doc(
        description="Filtra livros por faixa de preço",
        params={
            "min": "Preço mínimo",
            "max": "Preço máximo"
        }
    )
    def get(self):
        min_price = request.args.get("min", type=float)
        max_price = request.args.get("max", type=float)

        if min_price is None or max_price is None:
            api.abort(400, "Parâmetros min e max são obrigatórios")

        conn = get_db_connection()
        books = conn.execute("""
            SELECT * FROM books
            WHERE price BETWEEN ? AND ?
            ORDER BY price
        """, (min_price, max_price)).fetchall()
        conn.close()

        return books


@api.route("/stats")
class BooksStats(Resource):
    @api.doc(description="Estatísticas gerais da coleção de livros")
    def get(self):
        conn = get_db_connection()
        stats = conn.execute("""
            SELECT
                COUNT(*) AS total_books,
                ROUND(AVG(price), 2) AS avg_price,
                MIN(price) AS min_price,
                MAX(price) AS max_price,
                ROUND(AVG(rating), 2) AS avg_rating
            FROM books
        """).fetchone()
        conn.close()

        return dict(stats)
