from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from src.config.config import Config
from pathlib import Path

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Garante que o diretório do banco existe antes de qualquer tentativa de conexão
    db_path = Config.DB_PATH if isinstance(Config.DB_PATH, Path) else Path(Config.DB_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Inicializa extensões
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        # força criação do arquivo (caso nenhuma tabela exista ainda) e cria tabelas
        if not db_path.exists():
            db_path.touch()  # cria arquivo vazio se não existir
        db.create_all()

    return app