from flask import Flask
from flask_jwt_extended import JWTManager

from src.routes import register_blueprints
from src.config.config import Config
from src.models import User
from src.extensions import db


jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões
    db.init_app(app)
    jwt.init_app(app)

    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app