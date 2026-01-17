"""
Rota de health check - Verifica o status da aplicação.
"""

from flask import Blueprint, jsonify, current_app
from datetime import datetime, timezone
from src.services.books_service import BooksService
from src.services.auth_service import AuthService
from src.services.ml_service import MLService
from src.repository.books_repository import BooksRepository
from src.extensions import db
from sqlalchemy import text

health_bp = Blueprint('health', __name__)

books_service = BooksService()
auth_service = AuthService()
ml_service = MLService()
books_repository = BooksRepository()

start_time = datetime.now(timezone.utc)


@health_bp.route('', methods=['GET'])
def health_check():
    """
    Verifica o status de saúde da aplicação.
    
    ---
    tags:
      - Health
    responses:
      200:
        description: Aplicação está funcionando
        schema:
          type: object
          properties:
            status:
              type: string
              example: "OK"
    """
    return jsonify({"status": "OK"}), 200


@health_bp.route('/status', methods=['GET'])
def health_check_full_status():
    """
    Status completo da aplicação - Agregado de todos os health checks.
    
    ---
    tags:
      - Health
    responses:
      200:
        description: Status completo da aplicação
        schema:
          type: object
          properties:
            status:
              type: string
              example: "OK"
            version:
              type: string
            timestamp:
              type: string
            uptime_seconds:
              type: number
            components:
              type: object
              properties:
                database:
                  type: string
                jwt:
                  type: string
                services:
                  type: string
    """
    uptime = (datetime.now(timezone.utc) - start_time).total_seconds()
    components = {}
    overall_status = "OK"
    
    # Database - Users DB (via SQLAlchemy)
    try:
        db.session.execute(text('SELECT 1'))
        inspector_query = text("SELECT name FROM sqlite_master WHERE type='table'")
        tables = db.session.execute(inspector_query).fetchall()
        components["user_database"] = {"status": "OK", "tables": len(tables)}
    except Exception as e:
        components["user_database"] = {"status": "ERROR", "message": str(e)}
        overall_status = "DEGRADED"
    
    # Database - Books DB (via BooksRepository)
    try:
        books_session = books_repository.Session()
        try:
            books_session.execute(text('SELECT 1'))
            inspector_query = text("SELECT name FROM sqlite_master WHERE type='table'")
            tables = books_session.execute(inspector_query).fetchall()
            components["books_database"] = {"status": "OK", "tables": len(tables)}
        finally:
            books_session.close()
    except Exception as e:
        components["books_database"] = {"status": "ERROR", "message": str(e)}
        overall_status = "DEGRADED"
    
    # JWT
    try:
        if not current_app.config.get('JWT_SECRET_KEY'):
            raise Exception("JWT_SECRET_KEY não configurada")
        components["jwt"] = {"status": "OK"}
    except Exception as e:
        components["jwt"] = {"status": "ERROR", "message": str(e)}
        overall_status = "DEGRADED"
    
    # Books Service
    try:
        books = books_service.get_all_books()
        components["books_service"] = {
            "status": "OK",
            "books_count": len(books) if books else 0
        }
    except Exception as e:
        components["books_service"] = {"status": "ERROR", "message": str(e)}
        overall_status = "DEGRADED"
    
    # Auth Service
    try:
        users_count = len(auth_service.repo.get_all_users()) if hasattr(auth_service.repo, 'get_all_users') else 0
        components["auth_service"] = {
            "status": "OK",
            "users_count": users_count
        }
    except Exception as e:
        components["auth_service"] = {"status": "ERROR", "message": str(e)}
        overall_status = "DEGRADED"
    
    # ML Service
    try:
        features = ml_service.get_features()
        components["ml_service"] = {
            "status": "OK",
            "features_available": len(features) if features else 0
        }
    except Exception as e:
        components["ml_service"] = {"status": "ERROR", "message": str(e)}
        overall_status = "DEGRADED"
    
    return jsonify({
        "status": overall_status,
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_seconds": uptime,
        "components": components
    }), 200