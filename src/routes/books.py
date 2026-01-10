from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from src.services.books_service import BooksService

books_bp = Blueprint('books', __name__)

service = BooksService()

@books_bp.route('/', methods=['GET'])
@jwt_required()
def getAllBooks():
    booksTitles = service.get_books()
    return jsonify(booksTitles)

@books_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def getBookById(id):
    book = service.get_book_by_id(id)
    return jsonify(book)

@books_bp.route('/search', methods=['GET'])
@jwt_required()
def searchBooks():
    title = request.args.get('title')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    rating = request.args.get('rating')
    min_rating = request.args.get('min_rating', type=int)
    max_rating = request.args.get('max_rating', type=int)
    rating = request.args.get('rating')
    category = request.args.get('category')

    books = service.search_books(title, min_price, max_price, rating, min_rating, max_rating, category)
    return jsonify(books)

@books_bp.route('/categories', methods=['GET'])
@jwt_required()
def getCategories():
    categories = service.get_categories()
    return jsonify(categories)



