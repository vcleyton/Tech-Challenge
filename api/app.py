from flask import Flask, request
from flask_restx import Api
from flask_jwt_extended import JWTManager
import time
import os

from api.logger import logger

from api.routes.books import api as books_ns
from api.routes.categories import api as categories_ns
from api.routes.health import api as health_ns
from api.routes.stats import api as stats_ns
from api.routes.auth import api as auth_ns
from api.routes.ml import api as ml_ns
from api.routes.scraping import api as scraping_ns


def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret-key"  # em produção usar ENV
    app.config["RESTX_MASK_SWAGGER"] = False

    jwt = JWTManager(app)

    api = Api(
        app,
        title="Books Tech Challenge API",
        version="1.0",
        description="API pública para consulta de livros (Tech Challenge)",
        doc="/api/v1/",
        strict_slashes=False,
        authorizations={
            "Bearer Auth": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Digite: Bearer <seu_token_jwt>"
            }
        },
        security="Bearer Auth" 
    )
    
    api.add_namespace(books_ns, path="/api/v1/books")
    api.add_namespace(categories_ns, path="/api/v1/categories")
    api.add_namespace(health_ns, path="/api/v1/health")
    api.add_namespace(stats_ns, path="/api/v1/stats")
    api.add_namespace(auth_ns, path="/api/v1/auth")
    api.add_namespace(ml_ns, path="/api/v1/ml")
    api.add_namespace(scraping_ns, path="/api/v1/scraping")

    @app.before_request
    def log_request():
        request.start_time = time.time()
        logger.info(f"{request.method} {request.path}")

    @app.after_request
    def log_response(response):
        duration = time.time() - request.start_time
        logger.info(f"Response time: {duration:.4f}s")
        return response

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    #app = create_app()
    #app.run(debug=True)
