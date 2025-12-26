from flask import Blueprint, jsonify
from api.database import get_db_connection

ml_bp = Blueprint("ml", __name__, url_prefix="/api/v1/ml")

@ml_bp.route("/features", methods=["GET"])
def ml_features():
    conn = get_db_connection()
    books = conn.execute("""
        SELECT
            price,
            rating,
            CASE WHEN availability > 0 THEN 1 ELSE 0 END AS available
        FROM books
    """).fetchall()
    conn.close()

    return jsonify([dict(row) for row in books])

@ml_bp.route("/training-data", methods=["GET"])
def training_data():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()

    return jsonify([dict(row) for row in books])

@ml_bp.route("/predictions", methods=["POST"])
def receive_predictions():
    data = request.get_json()

    return jsonify({
        "msg": "Predições recebidas com sucesso",
        "received": data
    })
