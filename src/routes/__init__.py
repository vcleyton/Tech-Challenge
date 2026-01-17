"""
Módulo de rotas da aplicação.
Registra todas as blueprints e configura a documentação Swagger.
"""

from flasgger import Swagger
from flask_cors import CORS
from .health import health_bp
from .books import books_bp
from .stats import stats_bp
from .auth import auth_bp
from .ml import ml_bp

def register_blueprints(app):
    """
    Registra todas as Blueprints da aplicação.
    Também configura a documentação Swagger/OpenAPI.
    """

    # Configuração de CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Configuração do Swagger/Flasgger
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Tech Challenge API",
            "description": "API para gerenciamento de livros, autenticação e previsões de preço com Machine Learning",
            "version": "1.0.0",
            "contact": {
                "email": "support@techallenge.com"
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        }
    }, config={
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    })

    # Registra blueprints
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(books_bp, url_prefix='/books')
    app.register_blueprint(stats_bp, url_prefix='/stats')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ml_bp, url_prefix='/ml')

    return swagger
