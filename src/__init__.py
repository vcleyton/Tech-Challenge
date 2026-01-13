from flask import Flask, jsonify

from src.routes import register_blueprints
from src.config.config import Config
from src.extensions import db, jwt
from src.utils.exceptions import (
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ConflictError,
    DatabaseError,
    MLError
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)
    jwt.init_app(app)

    register_blueprints(app)

    # Registro de handlers de erro
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app):
    """
    Registra handlers para todas as exceções da aplicação.
    """
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        """Handler para erros de validação."""
        return jsonify({"message": str(e), "error": "ValidationError"}), 400
    
    @app.errorhandler(NotFoundError)
    def handle_not_found_error(e):
        """Handler para recursos não encontrados."""
        return jsonify({"message": str(e), "error": "NotFoundError"}), 404
    
    @app.errorhandler(UnauthorizedError)
    def handle_unauthorized_error(e):
        """Handler para erros de autenticação."""
        return jsonify({"message": str(e), "error": "UnauthorizedError"}), 401
    
    @app.errorhandler(ConflictError)
    def handle_conflict_error(e):
        """Handler para conflitos de dados."""
        return jsonify({"message": str(e), "error": "ConflictError"}), 409
    
    @app.errorhandler(MLError)
    def handle_ml_error(e):
        """Handler para erros do módulo de Machine Learning."""
        return jsonify({"message": str(e), "error": "MLError"}), 500
    
    @app.errorhandler(DatabaseError)
    def handle_database_error(e):
        """Handler para erros de banco de dados."""
        return jsonify({"message": str(e), "error": "DatabaseError"}), 500
    
    @app.errorhandler(400)
    def handle_bad_request(e):
        """Handler para requisições mal formadas."""
        return jsonify({"message": "Requisição inválida", "error": "BadRequest"}), 400
    
    @app.errorhandler(404)
    def handle_not_found(e):
        """Handler para endpoints não encontrados."""
        return jsonify({"message": "Endpoint não encontrado", "error": "NotFound"}), 404
    
    @app.errorhandler(500)
    def handle_internal_server_error(e):
        """Handler para erros internos do servidor."""
        return jsonify({"message": "Erro interno do servidor", "error": "InternalServerError"}), 500
