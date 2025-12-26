from flask import Flask
from flask_restx import Api

from api.routes.books import api as books_ns
from api.routes.categories import api as categories_ns
from api.routes.health import api as health_ns
from api.routes.categories import categories_bp
from api.routes.stats import stats_bp
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from api.routes.ml import ml_bp
from api.logger import logger
from flask import request
from api.routes.auth import auth_bp

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(ml_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(categories_bp)

# Chave secreta do JWT (em produção: variável de ambiente)
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path}")

import time

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_response(response):
    duration = time.time() - request.start_time
    logger.info(f"Response time: {duration:.4f}s")
    return response

@scraping_bp.route("/trigger", methods=["POST"])
@jwt_required()
def trigger_scraping():
    return jsonify({"msg": "Scraping iniciado com sucesso"})


def create_app():
    app = Flask(__name__)

    api = Api(
        app,
        title="Books Tech Challenge API",
        version="1.0",
        description="API pública para consulta de livros (Tech Challenge)"
    )

    # Registrando namespaces (rotas)
    api.add_namespace(books_ns, path="/api/v1/books")
    api.add_namespace(categories_ns, path="/api/v1/categories")
    api.add_namespace(health_ns, path="/api/v1/health")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
