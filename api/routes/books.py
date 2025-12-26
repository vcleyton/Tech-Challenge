from flask_restx import Namespace, Resource, fields
from flask import request
from api.database import get_db_connection
from flask import Blueprint, jsonify, request

# Blueprint corretamente definido
books_bp = Blueprint("books", __name__, url_prefix="/api/v1/books")
api = Namespace("books", description="Operações relacionadas a livros")

# Modelo Swagger (documentação)
book_model = api.model("Book", {
    "id": fields.Integer,
    "title": fields.String,
    "price": fields.Float,
    "rating": fields.Integer,
    "availability": fields.String,
    "category": fields.String,
    "image_url": fields.String,
    "product_url": fields.String
})


@api.route("/")
class BookList(Resource):
    @api.marshal_list_with(book_model)
    def get(self):
        """
        Lista todos os livros disponíveis.
        """
        conn = get_db_connection()
        books = conn.execute("SELECT * FROM books").fetchall()
        conn.close()
        return books


@api.route("/<int:book_id>")
class BookDetail(Resource):
    @api.marshal_with(book_model)
    def get(self, book_id):
        """
        Retorna detalhes de um livro pelo ID.
        """
        conn = get_db_connection()
        book = conn.execute(
            "SELECT * FROM books WHERE id = ?",
            (book_id,)
        ).fetchone()
        conn.close()

        if book is None:
            api.abort(404, "Livro não encontrado")

        return book


@api.route("/search")
class BookSearch(Resource):
    @api.marshal_list_with(book_model)
    def get(self):
        """
        Busca livros por título e/ou categoria.
        """
        title = request.args.get("title")
        category = request.args.get("category")

        query = "SELECT * FROM books WHERE 1=1"
        params = []

        if title:
            query += " AND title LIKE ?"
            params.append(f"%{title}%")

        if category:
            query += " AND category = ?"
            params.append(category)

        conn = get_db_connection()
        books = conn.execute(query, params).fetchall()
        conn.close()

        return books

@books_bp.route("/top-rated", methods=["GET"])
def top_rated_books():
    """
    Lista livros com melhor avaliação
    ---
    tags:
      - Books
    parameters:
      - name: limit
        in: query
        type: integer
        default: 10
    responses:
      200:
        description: Lista de livros mais bem avaliados
    """
    from flask import request

    limit = request.args.get("limit", default=10, type=int)

    conn = get_db_connection()
    cursor = conn.cursor()

    books = cursor.execute("""
        SELECT * FROM books
        WHERE rating = 5
        ORDER BY price ASC
        LIMIT ?
    """, (limit,)).fetchall()

    conn.close()

    return jsonify([dict(book) for book in books])

@books_bp.route("/price-range", methods=["GET"])
def books_by_price_range():
    """
    Filtra livros por faixa de preço
    ---
    tags:
      - Books
    parameters:
      - name: min
        in: query
        type: number
        required: true
      - name: max
        in: query
        type: number
        required: true
    responses:
      200:
        description: Lista de livros dentro da faixa de preço
    """
    from flask import request

    min_price = request.args.get("min", type=float)
    max_price = request.args.get("max", type=float)

    if min_price is None or max_price is None:
        return jsonify({"error": "Parâmetros min e max são obrigatórios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    books = cursor.execute("""
        SELECT * FROM books
        WHERE price BETWEEN ? AND ?
        ORDER BY price
    """, (min_price, max_price)).fetchall()

    conn.close()

    return jsonify([dict(book) for book in books])

@books_bp.route("/search", methods=["GET"])
def search_books():
    category = request.args.get("category")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    rating = request.args.get("rating", type=int)

    query = "SELECT * FROM books WHERE 1=1"
    params = []

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

    return jsonify([dict(book) for book in books])

@books_bp.route("/stats", methods=["GET"])
def books_stats():
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

    return jsonify(dict(stats))
